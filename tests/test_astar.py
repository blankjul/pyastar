import unittest

from pyastar.astar import AStar
from pyastar.examples.example_graph import create_sample_graph, heuristic_sample_graph
from pyastar.interface import GraphProblem


class TestAStar(unittest.TestCase):

    def test_sample_graph(self):
        G = create_sample_graph()
        ret = AStar(GraphProblem(G, "s", "g", heuristic_sample_graph), verbose=False).find()
        self.assertEqual(ret, (('s', 'd', 'e', 'g'), 7.0))


if __name__ == '__main__':
    unittest.main()
