import random

from pyastar.multi.exhaustive import exhaustive
from pyastar.multi.factory import create_layered_graph
from pyastar.multi.nds import Archive, nds

n_layers = 2
n_nodes_per_layer = 100
n_connections_per_node = 20

G = create_layered_graph(n_layers, n_nodes_per_layer, n_connections_per_node).costs_as_list()


# add one more weight to a graph
def add_cost_to_graph(G, n_costs):
    keys = list(G.edges.keys())
    for edge in keys:
        weights = G.edges[edge]
        while len(weights) < n_costs:
            weights.append(random.random())


MAX_NUMBER_OF_WEIGHTS = 20

if __name__ == '__main__':

    n_layers = 2
    n_nodes_per_layer = 100
    n_connections_per_node = 20

    G = create_layered_graph(n_layers, n_nodes_per_layer, n_connections_per_node).costs_as_list()

    n_costs = list(range(1, 21))
    n_nds_paths = []

    for n_cost in n_costs:
        add_cost_to_graph(G, n_cost)
        ret = exhaustive(G, "s", "g")

        I = nds([e["g"] for e in ret])

        val = len(I) / len(ret)
        n_nds_paths.append(val)

        print(n_cost, val)
