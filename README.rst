pyastar - A* Algorithm in Python
====================================================================

You can find a documentation of `pyastar` at: https://www.egr.msu.edu/coinlab/pyastar/


|travis| |python| |license|


.. |travis| image:: https://travis-ci.com/julesy89/pyastar.svg?branch=master
   :alt: build status
   :target: https://travis-ci.com/msu-coinlab/pymoo

.. |python| image:: https://img.shields.io/badge/python-3.6-blue.svg
   :alt: python 3.6

.. |license| image:: https://img.shields.io/badge/license-apache-orange.svg
   :alt: license apache
   :target: https://www.apache.org/licenses/LICENSE-2.0


Installation
====================================================================

The official release is always available at PyPi:

.. code:: bash

    pip install -U pyastar


Usage
==================================

Graph
----------------------------------

.. code:: python

    
    from pyastar.interface import astar_graph
    from pyastar.util.graph import WeightedGraph


    def create_sample_graph():
        G = WeightedGraph()

        G.add_node("s", "a", "b", "c", "d", "e", "g")
        G.add_edge("s", "a", 1.5)
        G.add_edge("a", "b", 2.0)
        G.add_edge("b", "c", 3.0)
        G.add_edge("c", "g", 4.0)
        G.add_edge("s", "d", 2.0)
        G.add_edge("d", "e", 3.0)
        G.add_edge("e", "g", 2.0)

        G.preprocess()

        return G


    def heuristic_sample_graph(node):
        D = {
            "s": None,
            "a": 4.0,
            "b": 4.0,
            "c": 4.0,
            "d": 4.0,
            "e": 4.0,
            "g": 0.0
        }

        return D[node]


    if __name__ == '__main__':
        G = create_sample_graph()
        ret = astar_graph(G, "s", "g", heuristic_sample_graph)
        print("Shortest Path:", ret)


Grid
----------------------------------

.. code:: python

    
    from pyastar.interface import astar_graph
    from pyastar.util.grid import Grid
    from pyastar.util.heuristics import manhatten_dist_2d

    grid = Grid(5, 5)
    grid.add_obstacle((3, 0), (3, 1))
    G = grid.to_graph()

    start = (4, 0)
    goal = (0, 4)

    ret = astar_graph(G, start, goal, lambda x: manhatten_dist_2d(x, goal))
    print("Shortest Path:", ret)




Contact
====================================================================

Feel free to contact me if you have any question:

| Julian Blank (blankjul [at] egr.msu.edu)
| Michigan State University
| Computational Optimization and Innovation Laboratory (COIN)
| East Lansing, MI 48824, USA