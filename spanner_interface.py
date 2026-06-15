from abc import ABC, abstractmethod
from typing import List, Optional, Callable

class ISpanner(ABC):

    @abstractmethod
    def generate_topology(self, nodes: Optional[List] = None) -> List[List[int]]:
        """Every spanner MUST implement this."""
        pass

    def get_routing_algorithm(self) -> Callable:
        """
        DEFAULT BEHAVIOR: Returns a basic compass routing function.
        Subclasses can override this if they have specialized routing.
        """
        print("Using system default: Compass Routing.")
        
        def compass_router(source: int, destination: int, current_node: int) -> int:
            # Placeholder for actual geometric compass routing math:
            # 1. Look at coordinates of neighbors
            # 2. Pick the neighbor closest in angle to the destination
            # 3. Return that neighbor's ID as the next hop
            return current_node  # Dummy fallback
            
        return compass_router