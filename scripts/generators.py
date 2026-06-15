#Some simple generators for the spanner network
import networkx as nx
import random

def random_nodes(n: int):
    #generate a random set of n nodes with coordinates in [0,1]^2
    graph = nx.Graph()
    for i in range(n):
        graph.add_node(i, coords=(random.random()*20, random.random()*20))
    return graph