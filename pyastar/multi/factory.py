import random

from pyastar.util.graph import WeightedGraph


def create_layer(nth, n_nodes):
    return [(nth, k) for k in range(n_nodes)]


def connect(layer_a, layer_b, n_connections):
    ret = []

    for node_b in layer_b:

        perm = list(layer_a)
        random.shuffle(perm)

        for node_a in perm[:min(len(perm), n_connections)]:
            ret.append((node_a, node_b))

    return ret


def create_fully_connected_graph(n_nodes):
    G = WeightedGraph(n_weights=1)

    G.add_node("s")
    for k in range(1, n_nodes - 1):
        G.add_node(k)
    G.add_node("g")

    for i in G.get_nodes():
        for j in G.get_nodes():
            if i != j:
                G.add_edge(i, j, [random.random()])

    G.preprocess()

    return G


def create_layered_graph(n_layers, n_nodes_per_layer, n_connections_per_node):
    layers = [(["s"], [])]

    n_layers += 2

    while len(layers) < n_layers:
        is_last_layer = len(layers) == n_layers - 1
        if is_last_layer:
            V = ["g"]
            last_E = layers[-1][0]
            E = connect(last_E, V, len(last_E))
        else:
            V = create_layer(len(layers), n_nodes_per_layer) if len(layers) < n_layers - 1 else ["g"]
            E = connect(layers[-1][0], V, n_connections_per_node)

        layers.append((V, E))

    G = WeightedGraph()

    for V, _ in layers:
        G.add_node(*V)

    for _, E in layers:
        for i, j in E:
            G.add_edge(i, j, random.random())

    G.preprocess()

    return G
