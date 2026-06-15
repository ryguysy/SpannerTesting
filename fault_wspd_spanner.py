# fault_wspd_spanner.py
from spanner_interface import ISpanner
from wspd_spanner import WspdSpanner  # Import the specific concrete class

class FaultWspdSpanner(ISpanner):
    # Lock the type hint down to ONLY accept WspdSpanner
    def __init__(self, base_wspd: WspdSpanner):
        self.base_graph = base_wspd

    def generate_topology(self):
        # 1. Grab the base WSPD structure
        matrix = self.base_graph.generate_topology()
        
        # 2. Safely run your specialized WSPD fault-tolerance math
        # because you are 100% guaranteed this is a WSPD graph
        wspd_matrix = self._apply_wspd_theorem(matrix)
        return wspd_matrix

    def _apply_wspd_theorem(self, matrix):
        # Your specific research math goes here
        return matrix
        
    #def get_routing_algorithm(self):