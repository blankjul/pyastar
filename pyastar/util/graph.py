import math


class WeightedGraph:

    def __init__(self,
                 undirected=True,
                 ) -> None:
        super().__init__()
        self.nodes = {}
        self.edges = {}
        self.undirected = undirected

    def get_nodes(self):
        return list(self.nodes.keys())

    def add_node(self, *args):
        for node in args:
            self.nodes[node] = []

    def remove_node(self, node):
        del self.nodes[node]
        edges = list(self.edges.keys())
        for key in edges:
            if key[0] == node or key[1] == node:
                del self.edges[key]

    def add_edge(self, i, j, c):
        self.edges[(i, j)] = c
        if not self.undirected:
            self.edges[(j, i)] = c

    def preprocess(self):

        # for each edge add the neighbors
        for (i, j), c in self.edges.items():
            if i in self.nodes and j in self.nodes:
                self.nodes[i].append(j)
                if not self.undirected:
                    self.nodes[j].append(i)
            else:
                raise Exception("Can not an edge to an unknown node!")

        # filter out duplicates in the neighbor list
        for node in list(self.nodes.keys()):
            H = set()
            entry = []
            for elem in self.nodes[node]:
                if elem not in H:
                    entry.append(elem)
                    H.add(elem)
            self.nodes[node] = entry

    def get_neighbors(self, node):
        for n in self.nodes[node]:
            yield n

    def get_distance(self, i, j):
        if (i, j) in self.edges:
            return self.edges[(i, j)]
        else:
            return math.inf

    def costs_as_list(self):
        for node in list(self.edges.keys()):
            self.edges[node] = [self.edges[node]]
        return self
