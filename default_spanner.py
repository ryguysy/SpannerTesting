# routing_spanner.py
class FaultTolerantRoutingSpanner(ISpanner):
    def generate_topology(self):
        return [[0, 1], [1, 0]]

    def get_routing_algorithm(self):
        # A dummy placeholder function
        def placeholder_router(source, dest):
            return f"# TODO: Custom routing from {source} to {dest}"
        
        return None #placeholder_router