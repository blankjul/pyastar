from pyastar.util.graph import WeightedGraph


class Grid:

    def __init__(self, width, height) -> None:
        super().__init__()
        self.width = width
        self.height = height
        self.obstacles = []

    def add_obstacle(self, *coords):
        [self.obstacles.append(coord) for coord in coords]

    def to_graph(self):
        G = WeightedGraph(symmetric=True)

        for i in range(self.width):
            for j in range(self.height):
                G.add_node((i, j))

                if i - 1 >= 0:
                    G.add_edge((i, j), (i - 1, j), 1)
                if j + 1 < self.height:
                    G.add_edge((i, j), (i, j + 1), 1)
                if i + 1 < self.width:
                    G.add_edge((i, j), (i + 1, j), 1)
                if j - 1 >= 0:
                    G.add_edge((i, j), (i, j - 1), 1)

        for obstacle in self.obstacles:
            G.remove_node(obstacle)

        G.preprocess()
        return G
