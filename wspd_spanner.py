from scripts.generators import random_nodes
import networkx as nx
import math
from typing import Optional, List
from spanner_interface import ISpanner

class ThetaSpanner(ISpanner):
    def __init__(self, s: int = 6):
        self.s = s

    def generate_topology(self, nodes: Optional[List] = random_nodes(5)):
        G_ = self.brute_force(nodes)
        return G_

    def brute_force(self, G_in: nx.Graph):

        G = G_in.copy()
        nlist = list(G.nodes())
                

                

        return G

    def get_routing_algorithm(self):
        return None