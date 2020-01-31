from abc import abstractmethod


class Problem:

    def __init__(self,
                 start,
                 goal=None,
                 n_costs=None) -> None:
        super().__init__()
        self.start = start
        self.goal = goal
        self.n_costs = n_costs

    def is_goal(self, node):
        return node == self.goal

    @abstractmethod
    def get_neighbors(self, node):
        pass

    @abstractmethod
    def get_costs(self, node_a, node_b):
        pass

    def get_heuristic(self, node):
        return 0

    def get_total(self, g, h):
        f = g
        if h is not None:
            f += h
        return f

