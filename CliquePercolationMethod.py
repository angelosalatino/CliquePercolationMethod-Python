#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from igraph import *

def clique_percolation_method(graph, k = 3):
    communities  = list()
    
    cliques = graph.cliques(min=k, max=k)
    num_cliques = len(cliques)
    
    edge_list = list()
    for i in range(0,num_cliques):
        for j in range(i+1, num_cliques):
            if len(set(list(cliques[i] + cliques[j]))) == k+1:
                edge_list.append((i,j))
    
    clique_graph = Graph(edge_list)
    clique_graph.vs["name"] = [i for i in range(0,num_cliques)]
    
    components = clique_graph.decompose()
    
    for component in components:
        members_list = [list(cliques[i["name"]]) for i in component.vs] 
        this_community = [item for sublist in members_list for item in sublist]
        communities.append(list(set(this_community)))
    
    return communities
    




def test():
    g = Graph([(0, 1), (0, 2), (0, 3), (1, 2), (2, 3), (3, 4), (3, 5), (4, 5), (4, 7), (4, 6), (5, 7), (5, 6), (6, 7), (6, 8)])
    summary(g)
    plot(g)
    cliques = clique_percolation_method(g,3)
    print("Cliques:")
    for count, comm in enumerate(communities):
        print("{}: {}".format(count,comm))

def test_karate():
    karate = Graph.Read_GraphML("karate.GraphML")
    summary(karate)
    communities = clique_percolation_method(karate,3)
    print("Cliques:")
    for count, comm in enumerate(communities):
        print("{}: {}".format(count,comm))