import networkx as nx
import matplotlib.pyplot as plt

from theta_spanner import ThetaSpanner
from fault_theta_spanner import FaultThetaSpanner

from wspd_spanner import WspdSpanner
from fault_wspd_spanner import FaultWspdSpanner

from orchestrator import BookSimOrchestrator

'''
# --- Experiment 1: Theta Fault Tolerance ---
base_theta = ThetaSpanner(k=4)
faulty_theta = FaultThetaSpanner(base_theta) # Valid!
orchestrator = BookSimOrchestrator(faulty_theta)
orchestrator.write_config("theta_experiment.cfg")

# --- Experiment 2: WSPD Fault Tolerance ---
base_wspd = WspdSpanner(separation_factor=2)
faulty_wspd = FaultWspdSpanner(base_wspd) # Valid!
orchestrator.set_spanner(faulty_wspd) 
orchestrator.write_config("wspd_experiment.cfg")
'''

def graph_example():
    # Initialize an empty undirected graph
    G = nx.Graph()

    # Add nodes
    G.add_node("Alice")
    G.add_nodes_from(["Bob", "Charlie", "David"])

    # Add edges (connections)
    G.add_edge("Alice", "Bob")
    G.add_edges_from([("Bob", "Charlie"), ("Charlie", "David"), ("David", "Alice")])

    print(f"Nodes: {G.nodes()}")
    print(f"Edges: {G.edges()}")

    # Position nodes using a spring layout algorithm
    pos = nx.spring_layout(G)

    # Draw the layout visually
    nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=1500, font_weight='bold')
    plt.show()
