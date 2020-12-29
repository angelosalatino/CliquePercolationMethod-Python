#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from igraph import *

def clique_percolation_method(graph, k = 3):
    communities  = list()
    
    cliques = graph.cliques(min=k, max=k)
    num_cliques = len(cliques)
    
    set_cliques = [set(i) for i in cliques]
    
    edge_list = list()
    for i in range(0,num_cliques):
        for j in range(i+1, num_cliques):
            if len(set_cliques[i].intersection(set_cliques[j])) == k-1:
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
    communities = clique_percolation_method(karate,3)
    print("Cliques:")
    for count, comm in enumerate(communities):
        print("{}: {}".format(count,comm))
