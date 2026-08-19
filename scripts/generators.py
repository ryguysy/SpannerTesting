#Some simple generators for the spanner network
import networkx as nx
import random
from spanner_interface import ISpanner

def random_nodes(n: int, scale: float = 5.0):
    #generate a random set of n nodes with coordinates in [0,n*scale]^2
    graph = nx.Graph()
    for i in range(n):
        graph.add_node(i, coords=(random.random()*n*scale, random.random()*n*scale))
    return graph

#simpleFTS generator
def simple_fts(base_spanner: ISpanner, k: int):
        #for each node p, we compute N_p, all nodes with distance at most k + 1 from p
        #for each node p, we compute E_p, all edges {p,q} s.t q is in N_p
        #we then return G' = (V, E') where E' is the union of all E_p

        G = base_spanner.topology

        _G = nx.Graph()
        _G.add_nodes_from(G.nodes(data=True))

        E = set()

        for p in G.nodes():

            N_p = set(nx.ego_graph(G, p, radius=k+1).nodes()) - {p}
            E_p = {(p, q) for q in N_p}
            E.update(E_p)

        _G.add_edges_from(E)
        return _G 