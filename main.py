import math

import matplotlib.pyplot as plt
import networkx as nx

from theta_spanner import ThetaSpanner
#from fault_theta_spanner import FaultThetaSpanner

from wspd_spanner import WspdSpanner
#from fault_wspd_spanner import FaultWspdSpanner

#from orchestrator import BookSimOrchestrator

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

def graph_positions(G):
    return {node: G.nodes[node]["coords"] for node in G.nodes()}


def draw_theta_cones(ax, pos, k, ray_length=5.0):
    cone_width = 2 * math.pi / k
    for node, (x, y) in pos.items():
        for i in range(k):
            angle = i * cone_width
            ax.plot(
                [x, x + ray_length * math.cos(angle)],
                [y, y + ray_length * math.sin(angle)],
                color="gray",
                linewidth=0.8,
                alpha=0.5,
                zorder=0,
            )


def theta_spanner_example():
    theta_spanner = ThetaSpanner()
    G_theta = theta_spanner.generate_topology()
    print(f"Theta Spanner: {G_theta.edges()}")
    print(f"Theta Spanner: {G_theta.nodes()}")

    pos = graph_positions(G_theta)
    fig, ax = plt.subplots()
    draw_theta_cones(ax, pos, theta_spanner.k)
    nx.draw(
        G_theta,
        pos,
        ax=ax,
        with_labels=True,
        node_color="skyblue",
        node_size=150,
        font_weight="bold",
    )
    ax.set_aspect("equal")
    plt.show()


def wspd_spanner_example():
    wspd_spanner = WspdSpanner()
    G_wspd = wspd_spanner.generate_topology()
    print(f"WSPD Spanner: {G_wspd.edges()}")
    print(f"WSPD Spanner: {G_wspd.nodes()}")
    pos = graph_positions(G_wspd)
    fig, ax = plt.subplots()
    nx.draw(
        G_wspd,
        pos,
        ax=ax,
        with_labels=True,
        node_color="skyblue",
        node_size=150,
        font_weight="bold",
    )
    ax.set_aspect("equal")
    plt.show()

#theta_spanner_example()
wspd_spanner_example()
