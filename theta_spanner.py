from scripts.generators import random_nodes
import networkx as nx
import math
from typing import Optional, List
from spanner_interface import ISpanner

class ThetaSpanner(ISpanner):
    def __init__(self, k: int = 6):
        self.k = k
        self.cone_width = 2 * math.pi / self.k

    def generate_topology(self, nodes: Optional[List] = random_nodes(5)):
        G_theta = self.brute_force_theta(nodes)
        return G_theta

    def brute_force_theta(self, G_in: nx.Graph):

        G = G_in.copy()
        nlist = list(G.nodes())


        for node1 in nlist:


            cone_map = {i: (None, math.inf, 1.0) for i in range(self.k)}
            #(neighbor, bisector dist, weight)
            coord1 = G.nodes[node1]['coords']

            for node2 in nlist:

                if node1 == node2:
                    continue

                coord2 = G.nodes[node2]['coords']

                #check what cone node2 is in with respect to node1
                angle = math.atan2(coord2[1] - coord1[1], coord2[0] - coord1[0])
                angle = (angle + 2 * math.pi) % (2 * math.pi)
                cone_index = int(angle // self.cone_width) % self.k

                #compute bisector angle and its x,y components
                bisector_angle = cone_index * self.cone_width + self.cone_width / 2
                bisector_x = math.cos(bisector_angle)
                bisector_y = math.sin(bisector_angle)

                #compute vector to node2 and its projection length onto the bisector
                vec_to_node2 = (coord2[0] - coord1[0], coord2[1] - coord1[1])
                proj_len = vec_to_node2[0] * bisector_x + vec_to_node2[1] * bisector_y

                

                if 0 < proj_len < cone_map[cone_index][1]:
                    #calculate true distance to node2
                    print(f"Update! | src: {node1} | dest: {node2} | cone: {cone_index} | bisector dist: {proj_len} | Replaced: {cone_map[cone_index][0]}")

                    true_dist = math.sqrt((coord2[0] - coord1[0])**2 + (coord2[1] - coord1[1])**2)
                    cone_map[cone_index] = (node2, proj_len, true_dist)
                else:
                    print(f"Nope!   | src: {node1} | dest: {node2} | cone: {cone_index}")
            
            for cone_id, (neighbor, bisector_dist, true_dist) in cone_map.items():
                if neighbor is not None:
                    G.add_edge(node1, neighbor, weight=true_dist)

                

                

        return G

    def get_routing_algorithm(self):
        return None