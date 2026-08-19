import math

import matplotlib.pyplot as plt
import networkx as nx

from spanner_interface import ISpanner

from theta_spanner import ThetaSpanner
#from fault_theta_spanner import FaultThetaSpanner

from wspd_spanner import WspdSpanner
#from fault_wspd_spanner import FaultWspdSpanner

from scripts.generators import random_nodes, simple_fts

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


def theta_spanner_example(k = 6, nodes = random_nodes(5)):
    spanner = ThetaSpanner(k=k, nodes=nodes)
    G_theta = spanner.topology
    print(f"Theta Spanner: {G_theta.edges()}")
    print(f"Theta Spanner: {G_theta.nodes()}")

    pos = graph_positions(G_theta)
    fig, ax = plt.subplots()
    draw_theta_cones(ax, pos, spanner.k)
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
    spanner = WspdSpanner()
    G_wspd = spanner.topology
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


def simple_fts_example(k = 6, nodes = random_nodes(5)):
    fts = simple_fts(spanner, k)
    print(f"Simple FTS: {fts.edges()}")
    print(f"Simple FTS: {fts.nodes()}")
    pos = graph_positions(fts)
    fig, ax = plt.subplots()
    nx.draw(fts, pos, ax=ax, with_labels=True, node_color="skyblue", node_size=150, font_weight="bold")
    ax.set_aspect("equal")
    plt.show()

#Generate nodes
nodes = random_nodes(n=10, scale=5.0)
spanner = ThetaSpanner(k=6, nodes=nodes)

theta_spanner_example(k=6, nodes = nodes)
simple_fts_example(k=1, nodes = nodes)
#wspd_spanner_example(separation_factor=2, nodes = nodes)
