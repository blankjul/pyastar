import unittest

from pyastar.interface import GraphProblem
from pyastar.multi.dmoastar import DMOAStar
from pyastar.multi.weights import uniform_weights
from tests.resources.biobj_graph_sm import create_graph


class TestDMOAStar(unittest.TestCase):

    def test_find_extremes(self):
        G = create_graph()

        algorithm = DMOAStar(GraphProblem(G, "1", "4"), uniform_weights(2, 10))
        algorithm.find_extremes()

        self.assertAlmostEqual(8.0, algorithm.extremes[0].opt[1])
        self.assertAlmostEqual(11.0, algorithm.extremes[1].opt[1])


    def test_find(self):
        G = create_graph()
        algorithm = DMOAStar(GraphProblem(G, "1", "4"), uniform_weights(2, 100))
        algorithm.find_extremes()

        algorithm.find()
        algorithm.finalize()

        print("test")


