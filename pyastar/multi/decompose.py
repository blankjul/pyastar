from pyastar.problem import Problem


class Decomposition:

    def __init__(self, ideal=None, nadir=None) -> None:
        super().__init__()
        self.ideal = ideal
        self.nadir = nadir

    def normalize(self, f):
        n = len(f)
        ideal, nadir = self.ideal, self.nadir

        if ideal is not None:
            f = [f[k] - ideal[k] for k in range(n)]

            if nadir is not None:
                for k in range(n):
                    norm = nadir[k] - ideal[k]
                    if norm > 0:
                        f[k] = f[k] / norm

        return f


class ASF(Decomposition):

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def calc(self, f, w):
        n = len(f)
        f = self.normalize(f)
        asf = max([f[k] * w[k] for k in range(n)])
        return asf


class DecomposedProblem(Problem):

    def __init__(self, problem, weights, decomposition) -> None:
        start, goal, n_costs = problem.start, problem.goal, problem.n_costs
        super().__init__(start, goal, n_costs)

        self.problem = problem
        self.weights = weights
        self.decomposition = decomposition

    def get_costs(self, node_a, node_b):
        return self.decomposition.calc(self.problem.get_costs(node_a, node_b), self.weights)

    def get_heuristic(self, node):
        return self.decomposition.calc(self.problem.get_heuristic(node), self.weights)

    def get_neighbors(self, node):
        return self.problem.get_neighbors(node)

    def is_goal(self, node):
        return self.problem.is_goal(node)




