from pyastar.util.pq import PriorityQueue


class AStar:

    def __init__(self,
                 start,
                 func_goal,
                 func_neighbors,
                 func_distance,
                 func_heuristic) -> None:

        super().__init__()

        self.start = start
        self.func_goal = func_goal
        self.func_neighbors = func_neighbors
        self.func_distance = func_distance
        self.func_heuristic = func_heuristic

        # the optimal path to be returned
        self.opt = None

        # initialize the open set as custom priority queue (implemented as a set)
        self.pq = PriorityQueue(func_sorted_by=lambda x: x['f'])
        h = self.func_heuristic(self.start)
        self.pq.push(self.start, {'g': 0, 'h': h, 'f': h})

        # map that keeps track of the optimal path found by storing the best predecessor
        self.dp = {}

        # keep track of all nodes that are already closed (to never visit a node twice)
        self.closed = set()

    def reconstruct_path(self, goal):
        ret = [goal]
        while ret[-1] != self.start:
            ret.append(self.dp[ret[-1]])
        return ret[::-1]

    def has_next(self):
        return not self.pq.empty() and self.opt is None

    def get_path(self):
        return self.opt

    def next(self):

        # pop the first element and get the f and g values
        node, entry = self.pq.pop()

        # mark this node to be visited by adding it to the closed set
        self.closed.add(node)

        # if the goal has been found - we know it is optimal if the heuristic is admissible
        if self.func_goal(node):
            self.opt = self.reconstruct_path(node)
            return
        else:
            self.extend(node, entry)

    def extend(self, node, entry):
        # for easier notation reference pq and dp directly
        pq, dp = self.pq, self.dp

        # get the f and g values from the entry
        f, g = entry['f'], entry['g']

        # expand the search for all neighbors
        for neighbor in self.func_neighbors(node):

            # if the neighbor has not been considered yet
            if neighbor not in self.closed:

                # g value of the neighbor - distance traveled so far
                neighbor_g = g + self.func_distance(node, neighbor)

                # current best q found to the neighbor - or infinity if not visited yet
                best_g = pq.get(neighbor)['g'] if pq.contains(neighbor) else float("inf")

                # if we have found a better solution than before (or never have been there when best_g is infinity)
                if neighbor_g < best_g:

                    # if we have been there - remove it from the priority queue because we have found a better one
                    if pq.contains(neighbor):
                        pq.remove(neighbor)

                    # store the first or new best predecessor of the neighbor
                    dp[neighbor] = node

                    # create a new entry containing the necessary information
                    entry = {'g': neighbor_g, 'f': neighbor_g + self.func_heuristic(neighbor)}

                    # and store the new improved entry
                    pq.push(neighbor, entry)

    def find(self):
        while self.has_next():
            self.next()
        return self.get_path()


def astar(start, func_goal, func_neighbors, func_distance, func_heuristic):
    return AStar(start, func_goal, func_neighbors, func_distance, func_heuristic).find()


def astar_graph(G, start, goal, func_heuristic):
    def func_neighbors(node):
        return G.get_neighbors(node)

    def func_distance(node_a, node_b):
        return G.get_distance(node_a, node_b)

    def func_goal(node):
        return node == goal

    return astar(start, func_goal, func_neighbors, func_distance, func_heuristic)
