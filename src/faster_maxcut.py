''' 
Faster exact algorithms for MaxCut on split graphs.
@author: Marko Lalovic
'''

import numpy as np
from sage.all import *

class SplitGraph:
    ''' Split graph with |C| = k and |I| = s. '''
    def __init__(self, k, s, edges):
        self.k = k
        self.s = s
        self.n = k + s
        self.edges = edges
        
    def plot(self, file_name=""):
        sage_g = Graph()
        sage_g.add_edges(self.edges)
        p = sage_g.graphplot(pos=get_pos(self.k, self.s))
        if file_name:
            p.plot().save(file_name)
        else:
            p.show()

def faster_mc(g):
    ''' Implementation of the algorithm for MaxCut on split graph g. '''
    if g.k <= g.n/2:
        # small clique C
        return faster_mc_1(g)
    else:
        # small independent set I
        return faster_mc_2(g)
    
def faster_mc_1(g):
    ''' Handles case 1: small clique C. '''
    set_C = Set(range(g.k))
    set_I = Set(range(g.k, g.n))

    max_cut_size = 0
    max_cut = None
    for set_C1 in Subsets(set_C):
        set_C2 = set_C.difference(set_C1)
        set_I1 = Set([v for v in set_I if check_condition(v, set_C1, set_C2, g)])
        set_I2 = set_I.difference(set_I1)
        
        cut = set_C1.union(set_I1), set_C2.union(set_I2)
        cut_size = get_cut_size(cut, g.edges)
        if cut_size > max_cut_size:
            max_cut_size = cut_size
            max_cut = cut
            
    return max_cut

def faster_mc_2(g):
    ''' Handles case 2: small independent set I. '''
    set_C = Set(range(g.k))
    set_I = Set(range(g.k, g.n))

    max_cut_size = 0
    max_cut = None
    for set_I1 in Subsets(set_I):
        set_I2 = set_I.difference(set_I1)
        sorted_C = np.argsort([-get_measure(v, set_I1, set_I2, g) for v in set_C])
        for m in range(g.k):
            set_C1 = Set(sorted_C[:m])
            set_C2 = set_C.difference(set_C1)
        
            cut = set_C1.union(set_I1), set_C2.union(set_I2)
            cut_size = get_cut_size(cut, g.edges)
            if cut_size > max_cut_size:
                max_cut_size = cut_size
                max_cut = cut
            
    return max_cut

def get_cut_size(partition, edges):
    ''' Returs the cut size |E(X, Y)| given partition (X, Y) and edges E. '''
    X, Y = partition
    size = 0
    for edge in edges:
        x, y = edge
        if ((x in X and y in Y) or (x in Y and y in X)):
            size += 1
    return size

def get_nbs(v, g):
    ''' Returns the neighbors of v in graph g. '''
    nbs = []
    for edge in g.edges:
        if v in edge:
            if v == edge[0]:
                nbs.append(edge[1])
            else:
                nbs.append(edge[0])
    return nbs
    
def check_condition(v, set_C1, set_C2, g):
    ''' Returns true if |N(v) \cap C_2| \geq |N(v) \cap C_1|. '''
    nbs_v = Set(get_nbs(v, g))
    return len(nbs_v.intersection(set_C2)) >= len(nbs_v.intersection(set_C1))

def get_measure(v, set_I1, set_I2, g):
    #TODO combine with check condition
    nbs_v = Set(get_nbs(v, g))
    return len(nbs_v.intersection(set_I2)) - len(nbs_v.intersection(set_I1))

def brute_mc(g):
    ''' Brute force algorithm for MaxCut tries all possible
    partitions of vertex set V of a given graph g. '''
    max_cut_size = 0
    max_cut = None

    edges = g.edges
    n = g.n

    for b in range(2**n):
        vec_A = [int(t) for t in reversed(list(bin(b)[2:].zfill(n)))]
        set_A = set(filter(lambda i: vec_A[i] == 1, list(range(n))))
        set_B = set(filter(lambda i: vec_A[i] == 0, list(range(n))))

        cut = (set_A, set_B)
        cut_size = get_cut_size(cut, edges)
        if cut_size > max_cut_size:
            max_cut_size = cut_size
            max_cut = cut

    return max_cut

def get_split_graph(k = 3, s = 3):
    ''' Generates a "random" connected split graph by creating a complete graph
    and adding vertices only connected to some random vertices of the clique. '''
    g = graphs.CompleteGraph(k)
    subsets = Subsets(Set(range(k)))
    for i in range(k, k + s):
        while True:
            # iterates until vertex i in I is connected to at least one vertex from C
            random_subset = subsets.random_element()
            if random_subset != set():
                # random_subset = non-empty set of vertices in C
                break
        g.add_edges([(i, j) for j in random_subset])
    
    assert g.is_split()
    edges = [(u, v) for (u, v, _) in g.edges()]
    return SplitGraph(k, s, edges)

def get_pos(k, s, eps_y=1):
    ''' Returns the positions of vertices of a split graph for ploting. '''
    K = graphs.CompleteGraph(k)
    K_layout = K.layout()
    K_layout_xy = list(K_layout.values())

    K_layout_y = [K_layout_xy[i][1] for i in range(k)]
    y_min = np.min(K_layout_y) - eps_y
    y_max = np.max(K_layout_y) + eps_y

    K_layout_x = [K_layout_xy[i][0] for i in range(k)]
    x_min = np.min(K_layout_x)
    x_max = np.max(K_layout_x)

    pos = K_layout
    x_coord = 2 * x_max - x_min
    y_coords = np.linspace(y_min, y_max, num = s)
    if x_max == x_min:
        x_coord = 2
    
    for i in range(k, k + s):
        pos[i] = (x_coord, y_coords[i - k])
    return pos