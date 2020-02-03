class Node:

    def __init__(self, problem, key) -> None:
        super().__init__()
        self.problem = problem
        self.key = key

        self.prev = None
        self.g = None
        self.h = None
        self.f = None

    def set_previous(self, prev):
        self.prev = prev

    def get_neighbors(self):
        return self.problem.get_neighbors(self.key)

    def calc_h(self):
        self.h = self.problem.get_heuristic(self.key)
        return self.h

    def calc_g(self):
        if self.prev is None:
            self.g = 0.0
        else:
            self.g = self.prev.g + self.problem.get_costs(self.prev.key, self.key)
        return self.g

    def calc_f(self):
        f = self.g
        if self.h is not None:
            f += self.h
        self.f = f
        return self.f

    def is_goal(self):
        return self.problem.is_goal(self.key)


class NodeFactory:

    def __init__(self, problem) -> None:
        super().__init__()
        self.problem = problem

    def create(self, key=None):
        if key is None:
            key = self.problem.start
        return Node(self.problem, key)
