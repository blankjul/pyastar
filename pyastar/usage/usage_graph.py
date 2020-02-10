from pyastar.interface import astar_graph
from pyastar.util.graph import WeightedGraph


def create_sample_graph():
    G = WeightedGraph()

    G.add_node("s", "a", "b", "c", "d", "e", "g")
    G.add_edge("s", "a", 1.5)
    G.add_edge("a", "b", 2.0)
    G.add_edge("b", "c", 3.0)
    G.add_edge("c", "g", 4.0)
    G.add_edge("s", "d", 2.0)
    G.add_edge("d", "e", 3.0)
    G.add_edge("e", "g", 2.0)

    G.preprocess()

    return G


def heuristic_sample_graph(node):
    D = {
        "s": None,
        "a": 4.0,
        "b": 4.0,
        "c": 4.0,
        "d": 4.0,
        "e": 4.0,
        "g": 0.0
    }

    return D[node]


if __name__ == '__main__':
    G = create_sample_graph()
    ret = astar_graph(G, "s", "g", heuristic_sample_graph)
    print("Shortest Path:", ret)
