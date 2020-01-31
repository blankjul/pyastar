from pyastar.astar import AStar
from pyastar.multi.decompose import DecomposedProblem, ASF
from pyastar.util.misc import evaluate_path


class DMOAStar:

    def __init__(self, problem, weights) -> None:
        super().__init__()
        self.problem = problem
        self.weights = weights

        self.ideal = None
        self.nadir = None

        self.extremes = None
        self.decomp = None

        self.opt = None

    def find_extremes(self):
        m = self.problem.n_costs
        self.extremes = []

        for k in range(m):
            w = [0.0 for _ in range(m)]
            w[k] = 1.0

            dp = DecomposedProblem(self.problem, w, ASF())
            algorithm = AStar(dp).initialize()
            self.extremes.append(algorithm)

        run_until_done(self.extremes)

        self.opt = [e.opt for e in self.extremes]

        self.ideal = [length for _, length in self.opt]
        self.ideal = [0 for _, length in self.opt]

        payoff = [evaluate_path(self.problem, path) for path, _ in self.opt]
        self.nadir = [max([payoff[k][j] for k in range(m)]) for j in range(m)]

    def find(self):
        _weights = [w for w in self.weights if all([w != e.problem.weights for e in self.extremes])]
        self.decomp = []

        for w in _weights:
            asf = ASF(ideal=self.ideal, nadir=self.nadir)
            dp = DecomposedProblem(self.problem, w, asf)
            algorithm = AStar(dp)
            self.decomp.append(algorithm)

            ret = algorithm.find()
            self.opt.append(ret)

    def finalize(self):

        opt = []
        H = set()

        for path, _ in self.opt:
            if path not in H:
                obj = evaluate_path(self.problem, path)
                opt.append((path, obj))
                H.add(path)

        self.opt = opt




    def find_(self):
        self.decomp = []

        asf = ASF(ideal=self.ideal, nadir=self.nadir)
        dp = DecomposedProblem(self.problem, [0.5, 0.5], asf)
        algorithm = AStar(dp)
        path, length = algorithm.find()

        for w in self.weights:
            asf = ASF(ideal=self.ideal, nadir=self.nadir)
            dp = DecomposedProblem(self.problem, w, asf)
            algorithm = AStar(dp).initialize()
            self.decomp.append(algorithm)

        while True:
            at_least_one_extension = False

            for algorithm in self.decomp:
                if algorithm.has_next():
                    algorithm.next()
                    at_least_one_extension = True

            if not at_least_one_extension:
                break

        print("test")


def run_until_done(algorithms):
    while True:
        at_least_one_extension = False

        for algorithm in algorithms:
            if algorithm.has_next():
                algorithm.next()
                at_least_one_extension = True

        if not at_least_one_extension:
            break
