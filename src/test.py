import unittest
from faster_maxcut import *
from sage.misc.prandom import randint # type: ignore

class TestMaxCut(unittest.TestCase):

    def test_mc(self):
        ntests = 100
        range_k = (1, 10)
        range_s = (1, 10)
        
        for _ in range(ntests):
            k = randint(range_k[0], range_k[1])
            s = randint(range_s[0], range_s[1])
            
            g = get_split_graph(k, s)
            
            brute_cut = brute_mc(g)
            faster_cut = faster_mc(g)
            
            brute_cut_size = get_cut_size(brute_cut, g.edges)
            faster_cut_size = get_cut_size(faster_cut, g.edges)       

            self.assertEqual(brute_cut_size, faster_cut_size, 'Not equal!')

if __name__ == '__main__':
    unittest.main()