import random
import unittest

from pyastar.interface import astar
from tests.resources.maze import make_maze, MazeSolver, MazeProblem
from ttictoc import TicToc


class TestAStarOnMaze(unittest.TestCase):

    def test_maze(self):
        size = 20
        random.seed(1)
        m = make_maze(size, size)
        w = len(m.split('\n')[0])
        h = len(m.split('\n'))

        start = (1, 1)  # we choose to start at the upper left corner
        goal = (w - 2, h - 2)  # we want to reach the lower right corner

        t = TicToc()
        t.tic()
        _path = list(MazeSolver(m).astar(start, goal))
        t.toc()
        # print("Github", t.elapsed)

        t.tic()
        path, length = astar(MazeProblem(m, start, goal))
        t.toc()
        # print("pyastar", t.elapsed)

        # self.assertEqual(len(_path), len(path))

        # print(drawmaze(m, list(path)))


if __name__ == '__main__':
    unittest.main()
