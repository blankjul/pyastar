from pyastar.interface import astar_graph
from pyastar.util.graph import WeightedGraph


def create_graph_with_heuristic():
    G = WeightedGraph(undirected=True)
    G.add_node("1", "2", "3", "4")
    G.add_edge("1", "2", 2)
    G.add_edge("1", "3", 4)
    G.add_edge("2", "3", 1)
    G.add_edge("3", "4", 3)
    G.preprocess()

    def heuristic(node):
        D = {
            "1": 6,
            "2": 4,
            "3": 1,
            "4": 0
        }

        return D[node]

    return G, heuristic


G, heuristic = create_graph_with_heuristic()

ret = astar_graph(G, "1", "4", heuristic, revisit_if_inconsistent=True, verbose=True)
print("Shortest Path:", ret)
