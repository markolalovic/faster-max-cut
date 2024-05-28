from faster_maxcut import *
from sage.misc.randstate import set_random_seed # type: ignore

def run_example():
    set_random_seed(1)
    
    k = 5 # size of a clique C
    s = 4 # size of an independent set I

    g = get_split_graph(k, s)
    g.plot("split-graph-example.svg")

    brute_cut = brute_mc(g)
    faster_cut = faster_mc(g)

    brute_cut_size = get_cut_size(brute_cut, g.edges)
    faster_cut_size = get_cut_size(faster_cut, g.edges)

    print('brute_cut  = {}  size = {}'.format(brute_cut,  brute_cut_size))
    print('faster_cut = {}  size = {}'.format(faster_cut, faster_cut_size))

if __name__ == '__main__':
    run_example()