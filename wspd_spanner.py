from scripts.generators import random_nodes
import networkx as nx
import math
from typing import Optional, List
from spanner_interface import ISpanner

class TreeNode:
    def __init__(self, value, nodes):
        self.value = value
        self.nodes = nodes
        self.left = None
        self.right = None

class BoundingBox:
    def __init__(self, min_corner, max_corner):
        self.min_corner = min_corner
        self.max_corner = max_corner
        self.width = max_corner[0] - min_corner[0]
        self.height = max_corner[1] - min_corner[1]
        self.center = ((min_corner[0] + max_corner[0]) / 2, (min_corner[1] + max_corner[1]) / 2)
        self.radius = math.sqrt(self.width**2 + self.height**2) / 2
        self.lmax = max(self.width, self.height)

class WspdSpanner(ISpanner):
    def __init__(self, separation_factor: int = 6):
        self.s = separation_factor

    def generate_topology(self, nodes: Optional[List] = random_nodes(5)):
        G_ = self.brute_force(nodes)
        return G_

    def _coords(self, G, node):
        return G.nodes[node]['coords']

    def _distance(self, G, node_a, node_b):
        ax, ay = self._coords(G, node_a)
        bx, by = self._coords(G, node_b)
        return math.hypot(ax - bx, ay - by)

    def _bbox_from_nodes(self, G, nodes):
        xs = [self._coords(G, n)[0] for n in nodes]
        ys = [self._coords(G, n)[1] for n in nodes]
        return BoundingBox((min(xs), min(ys)), (max(xs), max(ys)))

    def _closest_pair(self, G, nodes_a, nodes_b):
        best = None
        best_dist = math.inf
        for a in nodes_a:
            for b in nodes_b:
                dist = self._distance(G, a, b)
                if dist < best_dist:
                    best_dist = dist
                    best = (a, b)
        return best, best_dist

    def _well_separated(self, node_A, node_B, s):
        rho = max(node_A.value.radius, node_B.value.radius)
        center_dist = math.hypot(
            node_A.value.center[0] - node_B.value.center[0],
            node_A.value.center[1] - node_B.value.center[1],
        )
        return center_dist - 2 * rho >= s * rho

    def brute_force(self, G_in: nx.Graph):
        G = G_in.copy()
        nlist = list(G.nodes())

        if len(nlist) < 2:
            return G

        xlist = sorted(nlist, key=lambda n: self._coords(G, n)[0])
        ylist = sorted(nlist, key=lambda n: self._coords(G, n)[1])

        min_corner = (self._coords(G, xlist[0])[0], self._coords(G, ylist[0])[1])
        max_corner = (self._coords(G, xlist[-1])[0], self._coords(G, ylist[-1])[1])

        bbox = BoundingBox(min_corner, max_corner)
        root = TreeNode(bbox, nlist)
        self.build_tree(G, root)

        pair_list = []
        self._collect_wspd(root, self.s, pair_list)
        #print the pair list
        for pair in pair_list:
            print(f"Pair: {pair[0].nodes} - {pair[1].nodes}")

        for node_a, node_b in pair_list:
            pair, weight = self._closest_pair(G, node_a.nodes, node_b.nodes)
            if pair is not None:
                G.add_edge(pair[0], pair[1], weight=weight)

        return G

    def _collect_wspd(self, tree_node, s, pair_list):
        if tree_node.left is None or tree_node.right is None:
            return
        self.findWSPD(tree_node.left, tree_node.right, s, pair_list)
        self._collect_wspd(tree_node.left, s, pair_list)
        self._collect_wspd(tree_node.right, s, pair_list)

    def build_tree(self, G, tree_node):
        nodes = tree_node.nodes
        if len(nodes) <= 1:
            return

        if tree_node.value.width > tree_node.value.height:
            split_value = tree_node.value.center[0]
            idx = 0
        else:
            split_value = tree_node.value.center[1]
            idx = 1

        left_list = []
        right_list = []

        for node in nodes:
            if self._coords(G, node)[idx] < split_value:
                left_list.append(node)
            else:
                right_list.append(node)

        if not left_list or not right_list:
            sorted_nodes = sorted(nodes, key=lambda n: self._coords(G, n)[idx])
            mid = len(sorted_nodes) // 2
            left_list = sorted_nodes[:mid]
            right_list = sorted_nodes[mid:]

        if not left_list or not right_list:
            return

        left_bbox = self._bbox_from_nodes(G, left_list)
        right_bbox = self._bbox_from_nodes(G, right_list)

        tree_node.left = TreeNode(left_bbox, left_list)
        tree_node.right = TreeNode(right_bbox, right_list)

        self.build_tree(G, tree_node.left)
        self.build_tree(G, tree_node.right)

    def findWSPD(self, node_A, node_B, s, pair_list):
        if node_A is None or node_B is None:
            return

        if self._well_separated(node_A, node_B, s):
            pair_list.append((node_A, node_B))
        elif node_A.value.lmax <= node_B.value.lmax:
            if node_B.left is None or node_B.right is None:
                return
            self.findWSPD(node_A, node_B.left, s, pair_list)
            self.findWSPD(node_A, node_B.right, s, pair_list)
        else:
            if node_A.left is None or node_A.right is None:
                return
            self.findWSPD(node_A.left, node_B, s, pair_list)
            self.findWSPD(node_A.right, node_B, s, pair_list)

    def get_routing_algorithm(self):
        return None
