# faster-max-cut
A faster exact algorithm for the maximum cut problem on split graphs. The implementation is in `src/faster_maxcut.py`.

## Example
The script `src/example.py` generates an example of a split graph. The drawing is saved in the figures directory. The example of split graph with a clique of size `k = 5` and independent set of size `s = 4` is shown below:

![Split graph example](figures/split-graph-example.svg)

Next, it runs both the brute-force algorithm and the faster algorithm on the example, returning the same results:
```bash
$ sage src/example.py
# brute_cut  = ({1, 3, 5, 6, 7}, {0, 8, 2, 4})  size = 15
# faster_cut = ({0, 8, 2, 4}, {1, 3, 5, 6, 7})  size = 15
```

To test for correctness, the script `src/test.py` checks that both algorithms return the same results on 100 random split graphs with `k` and `s` between 1 and 10, successfully:
```bash
.
----------------------------------------------------------------------
Ran 1 test in 36.267s

OK
```
