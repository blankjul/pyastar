from pyastar.astar import AStar


class MOAStar(AStar):

    def __init__(self, problem) -> None:
        super().__init__()
        self.problem = problem


