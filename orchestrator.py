# orchestrator.py
class BookSimOrchestrator:
    def __init__(self, spanner: ISpanner):
        self.spanner = spanner

    def write_config(self, file_path: str):
        matrix = self.spanner.generate_topology()
        
        # Safely handle the unimplemented algorithm
        routing_logic = self.spanner.get_routing_algorithm()
        
        routing_string = f"routing_function = custom;\n# {routing_logic(0, 1)}"

        # Write to file
        config = [
            f"network_matrix = {str(matrix)};",
            routing_string
        ]
        print(f"Writing BookSim2 config with: {routing_string}")