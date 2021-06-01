from igraph import Graph, summary, plot
from functools import partial
from multiprocessing.pool import Pool
import time


def clique_percolation_method(graph, k = 3, workers = 1, attribute = None, verbose = False):
    """
    Function that implements the Clique Percolation Method (CPM) algorithm for 
    finding overlapping communities within networks, introduced by Palla et al. (2005).

    Parameters
    ----------
    graph : igraph object
        The igraph object containing the graph.
    k : int, optional
        Size of the clique. The default is 3.
    workers : int, optional
        Number of threads to allocate for running this algorithm. The default is 1.
    attribute : str, optional
        The attribute of the vertices to use for displaying nodes within the communities. 
        For displaying purposes, if vertices have names, the latter can be quite handy to figure out which node belongs to a certain community. 
        If no attribute is given, the algorithm will display their id. The default is None.
    verbose : bool, optional
        If set to True it shows status updates. The default is False.

    Raises
    ------
    TypeError
        If the types of the variables passed are incorrect.
    ValueError
        If the values of the variables passed are incorrect.

    Returns
    -------
    list
        Contains lists of communities (lists).

    """
    if not isinstance(graph,Graph):
            raise TypeError("The object graph must be an instance of the igraph class")    
    
    if not isinstance(k,int):
        raise TypeError("Expecting size of cliques (k) to be an integer")
        
    if not isinstance(workers,int):
            raise TypeError("Number of workers must be integer") 
            
    if workers < 1:
        raise ValueError("Expecting number of workers greater than or equal to 1")
        
    if attribute is not None:
        if not isinstance(attribute,str):
            raise TypeError("Expecting attribute to be a string")
            
        if attribute not in graph.vs.attributes():
            raise ValueError("Attribute {} in vertices does not exist".format(attribute))
        
    if not isinstance(verbose,bool):
        raise TypeError("Field verbose must be set to either True or False")
        
    communities  = list()
    
    if verbose:
        start_time = time.time()
    
    # FINDING CLIQUES
    cliques = graph.cliques(min=k, max=k)
    num_cliques = len(cliques)
    
    if verbose:
        print("Finished cliques --- %s seconds ---" % (time.time() - start_time))
        print("Cliques found %s" % (num_cliques))
        
    set_cliques = [set(i) for i in cliques]
    
    # FINDING CLIQUE GRAPH
    indices = list(range(num_cliques))

    edge_list = list()
    minimum = k-1
    annotate = partial(partial_clique_graph, set_cliques=set_cliques, minimum=minimum, num_cliques=num_cliques)
    
    pool = Pool(workers)
    edges = pool.map(annotate, indices)
    edge_list = [j for i in edges for j in i]
    
    if verbose:
        print("Finished comparison cliques --- %s seconds ---" % (time.time() - start_time))
    
    clique_graph = Graph(edge_list)
    clique_graph.vs["name"] = [i for i in range(0,num_cliques)]
    
    # FINDING CONNECTED COMPONENTS IN THE GRAPH
    components = clique_graph.decompose()
    
    # CREATING COMMUNITIES
    for component in components:
        members_list = [list(cliques[i["name"]]) for i in component.vs] 
        this_community = [item for sublist in members_list for item in sublist]
        communities.append(list(set(this_community)))
    
    if attribute is not None:
        communities_with_names = list()
        for community in communities:
            communities_with_names.append([graph.vs[element][attribute] for element in community])
        communities = communities_with_names
        
    if verbose:    
        print("Finished all --- %s seconds ---" % (time.time() - start_time))
        
    for comm in communities:
        print(len(comm))
        
    return communities


def partial_clique_graph(i, set_cliques, minimum, num_cliques):
    """
    Function that supports the creation of the clique graph, the second stage of CPM.
    This function is detached from the main function since it is parallelised 
    (based on the amout of workers).

    Parameters
    ----------
    i : integer
        The iterator for parallelisation.
    set_cliques : list(set)
        List containing all found cliques. Each clique is a set so it becomes easier to compare
    minimum : int
        Minimum overlapping between two cliques (size_of_cliques-1).
    num_cliques : int
        Number of cliques found in the graph.

    Returns
    -------
    edge_list : list
        List of edges belonging to the iterated node.

    """
    edge_list = list()
    this_set = set_cliques[i]
    for j in range(i+1, num_cliques):
        if len(this_set.intersection(set_cliques[j])) == minimum:
            edge_list.append((i,j))
    return edge_list    


def test():
    g = Graph()
    g.add_vertices(["1","2","3","4","5","6","7","8","9"])
    g.add_edges([("1", "2"), ("1", "3"), ("1", "4"), ("2", "3"), ("3", "4"), ("4", "5"), ("4", "6"), ("5", "6"), ("5", "8"), ("5", "7"), ("6", "8"), ("6", "7"), ("7", "8"), ("7", "9")])
    summary(g)
    plot(g)
    communities = clique_percolation_method(g,3)
    print("Cliques:")
    for count, comm in enumerate(communities):
        print("{}: {}".format(count,[g.vs[i]["name"] for i in comm]))


def test_karate():
    karate = Graph.Read_GraphML("karate.GraphML")
    summary(karate)
    communities = clique_percolation_method(karate,3,attribute="name")
    print("Cliques:")
    for count, comm in enumerate(communities):
        print("{}: {}".format(count,comm))
