from networkx import Graph

from parse import search
from networkx import (
    draw,
    get_node_attributes,
    draw_networkx_edge_labels,
    spring_layout,
    draw_networkx_labels,
    get_edge_attributes,
)
import matplotlib.pyplot as plt


def get_graph():
    lines = open("input.txt").read().splitlines()
    G = Graph()
    nodes = []
    nbr_vents_to_open = 0

    for l in lines:
        [name, rate] = search("Valve {:w} has flow rate={:d};", l)
        valves = [v[-2:] for v in l.split(" valve")[1].split(", ")]
        nodes.append({"name": name, "rate": rate, "valves": valves})
        if rate > 0:
            nbr_vents_to_open += 1
        G.add_node(name, rate=rate, name=name)

    print("Starting out with", len(G.nodes))

    for n in nodes:
        for v in n["valves"]:
            G.add_edge(n["name"], v, weight=1)

    # Optimize graph
    did_change = True
    while did_change:
        did_change = False
        for n in G.nodes:
            if len(list(G.neighbors(n))) == 2 and G.nodes[n]["rate"] == 0:
                neighs = list(G.neighbors(n))
                G.add_edge(
                    neighs[0],
                    neighs[1],
                    weight=G.get_edge_data(neighs[0], n)["weight"]
                    + G.get_edge_data(n, neighs[1])["weight"],
                )
                G.add_edge(
                    neighs[1],
                    neighs[0],
                    weight=G.get_edge_data(neighs[1], n)["weight"]
                    + G.get_edge_data(n, neighs[0])["weight"],
                )
                G.remove_node(n)
                did_change = True
                break

    print("After optimization nbr nodes:", len(G.nodes))
    return G, nbr_vents_to_open


def plot_graph(G):
    node_labels = get_node_attributes(G, "rate")
    edge_labels = get_edge_attributes(G, "weight")
    pos = spring_layout(G, scale=1)
    draw(G, pos, node_size=10)
    draw_networkx_labels(G, pos, font_size=2, labels=node_labels)
    draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=3)
    plt.savefig("plotgraph.png", dpi=1000, bbox_inches="tight")
