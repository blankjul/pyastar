from pyastar.astar import astar_graph
from pyastar.util.grid import Grid

grid = Grid(5, 5)
grid.add_obstacle((3, 0), (3, 1))
G = grid.to_graph()

start = (4, 0)
goal = (0, 4)


def manhatten_dist(pos_a, pos_b):
    return abs(pos_a[0] - pos_b[0]) + abs(pos_a[1] - pos_b[1])


ret = astar_graph(G, start, goal, lambda x: manhatten_dist(x, goal))
print("Shortest Path:", ret)
