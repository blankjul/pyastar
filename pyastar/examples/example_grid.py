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
