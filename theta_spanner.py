from scripts.generators import random_nodes
import networkx as nx
import math

class ThetaSpanner(ISpanner):
    def __init__(self, k: int):
        self.k = k

    def generate_topology(self):
        nodes = random_nodes(20)


    def brute_force_theta(self, G: nx.Graph):

        nlist = list(G.nodes())

        #compute angle split for each node (in radians 0-k)
        angles = [i * 2 * math.pi / k for i in range(k)]

        for node1 in nlist:

            cone_map = {i: None for i in range(k)}
            coord1 = G.nodes[node1]['coords']

            for node2 in nlist:

                if node1 == node2:
                    continue

                
                coord2 = G.nodes[node2]['coords']

                #check what cone node2 is in with respect to node1
                #compute projection of node2 onto the cone bisector of node1
                #update map so that current cone is key and value is the node2 if it is closer than the current value
                angle = math.atan2(coord2[1] - coord1[1], coord2[0] - coord1[0])
                cone_index = int(angle / (2 * math.pi / k))
                if cone_map[cone_index] is None:
                    cone_map[cone_index] = node2
                else:
                    #now we have to compare the projection of node2 onto the cone bisector of node1 with the current value
                    #if the new value is closer, update the map
                    old_coord = G.nodes[cone_map[cone_index]]['coords']
                    new_proj = coord2[0] * math.cos(angle) + coord2[1] * math.sin(angle)
                    old_proj = old_coord[0] * math.cos(angle) + old_coord[1] * math.sin(angle)
                    if new_proj < old_proj:
                        cone_map[cone_index] = node2

            for cone in cone_map:
                if cone_map[cone] is not None:
                    G.add_edge(node1, cone_map[cone], weight=math.sqrt((coord1[0] - G.nodes[cone_map[cone]]['coords'][0])**2 + (coord1[1] - G.nodes[cone_map[cone]]['coords'][1])**2))

        return G

    def get_routing_algorithm(self):
        return None