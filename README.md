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

# Reference
Palla, Gergely, Imre Derényi, Illés Farkas, and Tamás Vicsek. "Uncovering the overlapping community structure of complex networks in nature and society." Nature 435, no. 7043 (2005): 814-818.
