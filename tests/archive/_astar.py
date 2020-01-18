from pyastar.pq import PriorityQueue


def reconstruct_path(start, goal, path):
    ret = [goal]
    while ret[-1] != start:
        ret.append(path[ret[-1]])
    return ret[::-1]


def astar(start, goal, func_goal, func_neighbors, func_distance, func_heuristic):

    # initialize the open set as custom priority queue (implemented as a set)
    pq = PriorityQueue(func_sorted_by=lambda x: x['f'])
    pq.push(start, {'g': 0, 'f': func_heuristic(start)})

    # map that keeps track of the optimal path found by storing the best predecessor
    path = {}

    # keep track of all nodes that are already closed (to never visit a node twice)
    closed = set()

    # until the priority queue contains no values
    while not pq.empty():

        # pop the first element and get the f and g values
        key, entry = pq.pop()
        f, g = entry['f'], entry['g']

        # mark this node to be visited by adding it to the closed set
        closed.add(key)

        # if the goal has been found - we know it is optimal if the heuristic is admissible
        if func_goal(key, goal):
            return reconstruct_path(start, goal, path)

        # expand the search for all neighbors
        for n in func_neighbors(key):

            # if the neighbor has not been considered yet
            if n not in closed:

                # g value of the neighbor - distance traveled so far
                n_g = g + func_distance(key, n)

                # current best q found to the neighbor - or infinity if not visited yet
                best_g = pq.get(n)['g'] if pq.contains(n) else float("inf")

                # if we have found a better solution than before (or never have been there when best_g is infinity)
                if n_g < best_g:

                    # if we have been there - remove it from the priority queue because we have found a better one
                    if pq.contains(n):
                        pq.remove(n)

                    # store the first or new best predecessor of the neighbor
                    path[n] = key

                    # create a new entry containing the necessary information
                    entry = {'g': n_g, 'f': n_g + func_heuristic(n)}

                    # and store the new improved entry
                    pq.push(n, entry)

    return None


def astar_graph(G, start, goal, func_heuristic):
    def func_neighbors(node):
        return G.get_neighbors(node)

    def func_distance(node_a, node_b):
        return G.get_distance(node_a, node_b)

    def func_goal(node, goal):
        return node == goal

    return astar(start, goal, func_goal, func_neighbors, func_distance, func_heuristic)
