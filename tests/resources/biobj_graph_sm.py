from pyastar.util.graph import WeightedGraph


def create_graph():
    G = WeightedGraph()

    G.add_node("1", "21", "22", "23", "31", "32", "33", "4")

    G.add_edge("1", "21", [5, 2])
    G.add_edge("1", "22", [9, 8])
    G.add_edge("1", "23", [3, 8])

    G.add_edge("21", "31", [5, 2])
    G.add_edge("21", "32", [8, 7])
    G.add_edge("22", "32", [9, 9])
    G.add_edge("23", "32", [4, 8])
    G.add_edge("23", "33", [2, 1])

    G.add_edge("31", "4", [5, 7])
    G.add_edge("32", "4", [1, 7])
    G.add_edge("33", "4", [6, 9])

    G.preprocess()

    return G
