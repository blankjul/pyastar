from pyastar.astar import AStar
from pyastar.problem import Problem


class GraphProblem(Problem):

    def __init__(self, graph, start, goal, func_heuristic=None) -> None:
        super().__init__(start, goal=goal)
        self.graph = graph
        self.func_heuristic = func_heuristic

        if graph.edges is None or len(graph.edges) == 0:
            raise Exception("Supplied graph does not have any edges.")
        else:
            entry = next(iter(graph.edges))
            edge = graph.edges[entry]
            if isinstance(edge, list) or isinstance(edge, tuple):
                self.n_costs = len(edge)

    def get_neighbors(self, node):
        return self.graph.get_neighbors(node)

    def get_costs(self, node_a, node_b):
        if (node_a, node_b) in self.graph.edges:
            return self.graph.get_distance(node_a, node_b)
        else:
            if self.n_costs is None:
                return float("inf")
            else:
                return [float("inf") for _ in range(self.n_costs)]

    def get_heuristic(self, node):
        if self.func_heuristic is None:
            if self.n_costs is None:
                return 0.0
            else:
                return [0.0 for _ in range(self.n_costs)]
        else:
            return self.func_heuristic(node)


def astar_graph(graph, start, goal, func_heuristic=None, **kwargs):
    problem = GraphProblem(graph, start, goal, func_heuristic=func_heuristic)
    return AStar(problem, **kwargs).find()
