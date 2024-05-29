# faster-max-cut
A faster exact algorithm for the maximum cut problem on split graphs. The implementation is in `src/faster_maxcut.py`.

## Example
Generate an example of a split graph:
```python
from src.faster_maxcut import *
from sage.misc.randstate import set_random_seed

set_random_seed(1)

k = 5 # size of a clique C
s = 4 # size of an independent set I

g = get_split_graph(k, s) # generates a random connected split graph
g.plot("./figures/split-graph-example.svg")
```

The example of split graph with a clique of size `k = 5` and independent set of size `s = 4` is shown below:

![Split graph example](figures/split-graph-example.svg)

Next, runing both the brute-force algorithm and the faster algorithm on the example:
```python
brute_cut = brute_mc(g)
faster_cut = faster_mc(g)
```

Both algorithms find a cut of the same size:
```python
brute_cut_size = get_cut_size(brute_cut, g.edges)
faster_cut_size = get_cut_size(faster_cut, g.edges)
print('brute_cut  = {}  size = {}'.format(brute_cut,  brute_cut_size))
print('faster_cut = {}  size = {}'.format(faster_cut, faster_cut_size))
# brute_cut  = ({1, 3, 5, 6, 7}, {0, 8, 2, 4})  size = 15
# faster_cut = ({0, 8, 2, 4}, {1, 3, 5, 6, 7})  size = 15
```

## Test
To test for correctness, the script `src/test.py` checks that both algorithms find a cut of the same size on 100 random split graphs with `k` and `s` between 1 and 10, successfully:
```bash
$ ./src/test.py
.
----------------------------------------------------------------------
Ran 1 test in 36.267s

OK
```

Tested using Python 3.12.3 and SageMath version 10.3.
