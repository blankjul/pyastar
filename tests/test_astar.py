import random
import unittest

from pyastar.astar import AStar
from pyastar.examples.example_graph import create_sample_graph, heuristic_sample_graph
from pyastar.interface import GraphProblem, astar_graph
from pyastar.util.factory import create_layered_graph
from tests.resources.graph_inconsistent import create_graph_with_inconsistent_heuristic


class TestAStar(unittest.TestCase):

    def test_sample_graph(self):
        G = create_sample_graph()
        ret = AStar(GraphProblem(G, "s", "g", heuristic_sample_graph)).find()
        self.assertEqual(ret, (('s', 'd', 'e', 'g'), 7.0))

    def test_inconsistent_and_disabled(self):
        G, heuristic = create_graph_with_inconsistent_heuristic()
        path, costs = astar_graph(G, "1", "4", heuristic, heuristic_is_inconsistent=False)
        self.assertAlmostEqual(costs, 7.0)

    def test_inconsistent_and_enabled(self):
        G, heuristic = create_graph_with_inconsistent_heuristic()
        path, costs = astar_graph(G, "1", "4", heuristic, heuristic_is_inconsistent=True)
        self.assertAlmostEqual(costs, 6.0)

    def test__truncation(self):
        G = create_layered_graph(10, 100, 20)

        problem = GraphProblem(G, "s", "g")
        astar = AStar(problem, open_set_max_size=200, open_set_truncate_size=25).initialize()
        while astar.has_next():
            astar.next()
            # print(astar.open_set.size())
            self.assertTrue(astar.open_set.size() <= 200)





if __name__ == '__main__':
    unittest.main()
