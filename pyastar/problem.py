from abc import abstractmethod


class Problem:

    def __init__(self,
                 start,
                 goal=None) -> None:
        super().__init__()
        self.start = start
        self.goal = goal

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
