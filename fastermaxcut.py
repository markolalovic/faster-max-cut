#!/usr/bin/python3.8
# -*- coding: utf-8 -*-
'''fastermaxcut.py: A faster exact algorithm for Max-Cut currently for split graphs only. '''

import matplotlib.pyplot as plt
import numpy as np
import networkx as nx
from random import randrange
from random import sample

class Graph:
    ''' (k,s)-split graph. '''
    def __init__(self, k, s, edges):
        self.k = k
        self.s = s
        self.n = k + s
        self.edges = edges

def draw(g, name):
    graph = nx.Graph()
    graph.add_edges_from(g.edges)
    plt.figure(figsize=(5, 2.5))
    nx.draw(graph, pos=nx.spring_layout(graph), with_labels = True)
    plt.savefig('./figures/' + name + '_drawing.png',
                format="PNG", dpi=300, bbox_inches='tight')
    plt.close()

def generate_graph(k, s):
    ''' Generates a random (k, s)-split graph for tests. '''
    edges_comp = [] # for complete part
    for i in range(k):
        for j in range(i + 1, k):
            edges_comp.append((i, j))

    while True: ## try until we get graph on n = k + s vertices
        edges_bip = [] # for independent part
        for i in range(s):
            degree = randrange(k) # should be between 0 and k - 1
            neighbors = sample(list(range(k)), degree)
            for neighbor in neighbors:
                edges_bip.append((k + i, neighbor))

        vertices = set()
        edges = edges_comp + edges_bip
        for edge in edges:
            u, v = edge
            vertices.add(u)
            vertices.add(v)

        if len(vertices) == k + s:
            g = Graph(k, s, edges)
            return(g)

def cutvalue(X, Y, edges):
    ''' Returs the cut value |[X, Y]| of a given bipartition (X, Y) and given edges. '''
    cutv = 0
    for edge in edges:
        x, y = edge
        if ((x in X and y in Y) or (x in Y and y in X)):
            cutv += 1
    return cutv

def brute_mc(g):
    ''' Brute force algorithm that solves Max-Cut problem by checking all possible
    bipartitions (A, B) of vertex set V of given graph g. '''

    maxval = 0
    maxbpt = None

    edges = g.edges
    n = g.n

    for b in range(2**n):
        vec_A = [int(t) for t in reversed(list(bin(b)[2:].zfill(n)))]
        set_A = set(filter(lambda i: vec_A[i] == 1, list(range(n))))
        set_B = set(filter(lambda i: vec_A[i] == 0, list(range(n))))

        cutv = cutvalue(set_A, set_B, edges)
        if cutv > maxval:
            maxval = cutv
            maxbpt = (set_A, set_B)

    return maxval, maxbpt

def faster_mc(g):
    ''' Implementation of the algorithm. '''

    maxval = 0
    maxbpt = None

    edges = g.edges
    k = g.k
    s = g.s
    n = g.n

    ## in case of a small clique and large independent set
    ## expand all possible clique bipartitions (A, B)
    if k <= n/2:
        ## check each bipartition (A, B) of clique C
        for b in range(2**k):
            vec_A = [int(t) for t in reversed(list(bin(b)[2:].zfill(k)))]
            set_A = set(filter(lambda i: vec_A[i] == 1, list(range(k))))
            set_B = set(filter(lambda i: vec_A[i] == 0, list(range(k))))

            ## compute the table
            set_S = set()
            set_T = set()
            for j in range(k, k + s):
                ## for each vertex u_j from independent set I
                ## count the neighbors in sets A and B
                neighbors = set()
                for edge in edges:
                    u, v = edge
                    if u == j:
                        neighbors.add(v)
                    if v == j:
                        neighbors.add(u)
                    neighbors_A = set_A.intersection(neighbors)
                    neighbors_B = set_B.intersection(neighbors)

                ## put vertex u_j in set that maximizes the cut
                if len(neighbors_A) >= len(neighbors_B):
                    set_T.add(j)
                else:
                    set_S.add(j)

            ## compute the cut value of bipartition (AuS, BuT) and take the maximum
            set_X = set_A.union(set_S)
            set_Y = set_B.union(set_T)
            cutv = cutvalue(set_X, set_Y, edges)
            if  cutv > maxval:
                maxval = cutv
                maxbpt = (set_X, set_Y)

        return maxval, maxbpt

    ## in case of a large clique and small independent set
    ## expand all possible independent set bipartitions (S, T)
    else:
        ## for each bipartition (S, T) of independent set I
        ## find a maximum cut bipartition (A, B) of clique set C
        set_I = list(range(k, k+s))
        set_C = set(list(range(k)))
        for b in range(2**s):
            vec_S = [int(t) for t in reversed(list(bin(b)[2:].zfill(s)))]
            set_S = set([set_I[j] for j in range(s) if vec_S[j] == 1])
            set_T = set([set_I[j] for j in range(s) if vec_S[j] == 0])

            ## compute the table
            table = np.zeros((k, 2))
            for j in range(k):
                ## for each vertex v_j from clique C
                ## count the neighbors in sets S and T
                neighbors = set()
                for edge in edges:
                    u, v = edge
                    if u == j:
                        neighbors.add(v)
                    if v == j:
                        neighbors.add(u)
                    n_S = len(set_S.intersection(neighbors))
                    n_T = len(set_T.intersection(neighbors))
                    table[j, :] = [n_S, n_T]

            ## compute the difference N_S - N_T and use this difference to
            ## sort the vertices from clique C: v_{(1)}, v_{(2)}, ..., v_{(k)}
            ## this are the candidates for each size i of set A
            candidates = list(np.argsort(-(table[:, 1] - table[:, 0])))

            ## dynamically determine the best size i of set A
            ## by going over all set sizes i = 0, 1, ..., k
            for i in range(k):
                ## for fixed set size |A| = i
                ## we only need to consider A = {v_(1), v_(2), ..., v_(i)}
                ## because putting vertex v_j with N_S - N_T smaller than v_(i) in A
                ## would result in lower cut value
                set_A = set(candidates[:i])
                set_B = set_C.difference(set_A)

                ## compute the cut value of bipartition (AuS, BuT) and take the maximum
                set_X = set_A.union(set_S)
                set_Y = set_B.union(set_T)
                cutv = cutvalue(set_X, set_Y, edges)
                if cutv > maxval:
                    maxval = cutv
                    maxbpt = (set_X, set_Y)

        return maxval, maxbpt

def test(nsims, range_k, range_s):
    print("Running brute force and faster algorithm on " + str(nsims) + " tests:")
    for nsim in range(nsims):
        k = 2 + randrange(range_k)
        s = 1 + randrange(range_s)
        g = generate_graph(k, s)

        mc_b, bp_b = brute_mc(g)
        print('.', end = '')
        mc_s, bp_s = faster_mc(g)
        print('*', end = '')

        if mc_b != mc_s:
            print('Not equal: ')
            print(bp_b, bp_s)
            print(g.edges)
            draw(g)

    print("Done")

def example(k, s):
    g = generate_graph(k, s)
    draw(g, "(4,3)-split-graph-example")
    print(brute_mc(g))
    print(faster_mc(g))

if __name__ == '__main__':
    #example(4, 3)
    test(1000, 8, 9)
