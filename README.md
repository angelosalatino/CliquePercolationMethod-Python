# CliquePercolationMethod-Python
Clique Percolation Method (CPM) is an algorithm for finding overlapping communities within networks, intruduced by Palla et al. (2005, see references). This implementation in Python, firstly detects communities of size k, then creates a clique graph. Each community will be represented by each connected component in the clique graph.

# Algorithm
The algorithm performs the following steps:

1- first find all cliques of size k in the graph <br />
2- then create graph where nodes are cliques of size k <br />
3- add edges if two nodes (cliques) share k-1 common nodes <br />
4- each connected component is a community <br />

# Main Implementations
* clique_percolation_method(graph, k = 3): Implementation of the Clique Percolation Method 

It requires igraph library:
```
pip install python-igraph
```

# Run
In this version, the main script contains some test functionalities that help on how to get going with this algorithm.
```
import CliquePercolationMethod as cpm

cpm.text()
# or 
cpm.test_karate()
```

# Parameters
* **graph** : igraph object
    The _igraph object_ containing the graph.
* **k** : int, optional
    Size of the clique. The default is _3_.
* **workers** : int, optional
    Number of threads to allocate for running this algorithm. The default is _1_.
* **attribute** : str, optional
    The attribute of the vertices to use for displaying nodes within the communities. 
    For displaying purposes, if vertices have names, the latter can be quite handy to figure out which node belongs to a certain community. 
    If no attribute is given, the algorithm will display their id. The default is _None_.
* **verbose** : bool, optional
    If set to _True_ it shows status updates. The default is _False_.

# Reference
Palla, Gergely, Imre Derényi, Illés Farkas, and Tamás Vicsek. "Uncovering the overlapping community structure of complex networks in nature and society." Nature 435, no. 7043 (2005): 814-818.
