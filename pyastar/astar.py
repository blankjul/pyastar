from pyastar.util.pq import PriorityQueue


class AStar:

    def __init__(self,
                 problem,
                 revisit_if_inconsistent=False,
                 verbose=False):

        self.problem = problem
        self.revisit_if_inconsistent = revisit_if_inconsistent
        self.verbose = verbose

        # the optimal path to be returned
        self.opt = None

        # the current node that is processed
        self.current = None
        self.extended = None

        # initialize the open set as custom priority queue (implemented as a set)
        self.pq = PriorityQueue(func_sorted_by=lambda x: x['f'])

        # keep track of all nodes that are already closed - including their g values
        self.closed = {}

    def initialize(self):
        start = self.problem.start
        g = 0
        h = self.problem.get_heuristic(start)
        f = self.problem.get_total(g, h)
        self.pq.push(start, {'g': g, 'h': h, 'f': f, 'previous': None})
        return self

    def pop(self):
        _open, _closed = self.pq, self.closed

        # initially set the current value to non - to check if something was set or not
        self.current = None

        # pop the first element - if heuristic is inconsistent we might skip nodes that have be revisited
        if not self.revisit_if_inconsistent:
            self.current = _open.pop()

        else:
            while not _open.empty():
                node, entry = _open.pop()

                # either take a node if not in closed at all or if the closed not was not better or equally good than it
                if node not in _closed or entry["g"] < _closed[node]["g"]:
                    self.current = (node, entry)
                    break

        return self.current is not None

    def next(self):

        # retrieve the first element - it set to current in this class
        success = self.pop()

        # if no element could be found to be processed
        if success:

            # get the current information of the node
            node, entry = self.current

            # get access to the open and closed set
            _open, _closed = self.pq, self.closed

            # if the verbose flag is set to true, print some information about the current status
            if self.verbose:
                self.info()

            # mark this node to be visited by adding it to the closed set
            self.closed[node] = entry

            # if the goal has been found - we know it is optimal if the heuristic is admissible
            if self.problem.is_goal(node):
                self.opt = self.reconstruct_path()
                return
            else:
                # reset the node that has been extended in the last step
                self.extended = []
                for neighbor in self.problem.get_neighbors(node):
                    is_better, entry = self.is_node_better(neighbor)
                    if is_better:
                        self.extended.append((neighbor, entry))

                self.extend()

    def is_node_better(self, neighbor):
        _current, _open, _closed = self.current, self.pq, self.closed
        node, g, f = _current[0], _current[1]['g'], _current[1]['f']

        entry = {}

        # the following code snippets decides whether the node should be added to the open set or not
        if neighbor in _closed:

            # if the heuristic is consistent a node is visited only once - therefore it can not be improved
            if not self.revisit_if_inconsistent:
                is_better = False

            # if inconsistent and the flag is activated check whether we have improved compared to a closed node
            else:
                entry["g"] = g + self.problem.get_costs(node, neighbor)
                is_better = entry["g"] < _closed[neighbor]['g']

        # if a node has never been visited yet
        else:
            entry["g"] = g + self.problem.get_costs(node, neighbor)

            if not _open.contains(neighbor):
                is_better = True
            else:
                is_better = entry["g"] < _open.get(neighbor)['g']

        return is_better, entry

    def extend(self):
        _node, _open = self.current[0], self.pq

        # expand the search for all neighbors
        for neighbor, entry in self.extended:

            # if we have been there - remove it from the priority queue because we have found a better one
            if _open.contains(neighbor):
                _open.remove(neighbor)

            # create a new entry containing the necessary information
            if "h" not in entry:
                entry["h"] = self.problem.get_heuristic(neighbor)
            if "f" not in entry:
                entry["f"] = self.problem.get_total(entry["g"], entry["h"])

            entry["previous"] = _node

            # and store the new improved entry
            _open.push(neighbor, entry)

    def find(self, return_path_length=True):
        self.initialize()

        while self.has_next():
            self.next()

        if self.opt is None:
            if return_path_length:
                return None, None
            else:
                return None
        else:
            if return_path_length:
                return self.opt
            else:
                return self.opt[0]

    def reconstruct_path(self):
        goal, _ = self.current

        path = [goal]
        while path[-1] != self.problem.start:
            path.append(self.closed[path[-1]]["previous"])
        path = path[::-1]

        costs = 0
        for k in range(len(path) - 1):
            costs += self.problem.get_costs(path[k], path[k + 1])

        return tuple(path), costs

    def has_next(self):
        return not self.pq.empty() and self.opt is None

    def get_path(self):
        return self.opt

    def info(self):
        from copy import deepcopy
        _current, _open, _closed = self.current, deepcopy(self.pq), self.closed

        print("CURRENT")
        print(_current[0], "->", _current[1])
        print()

        print("OPEN SET")
        for k in range(min(10, _open.size())):
            node, entry = _open.pop()
            print(node, "->", entry)
        print()

        print("CLOSED SET")
        for node, entry in _closed.items():
            print(node, "->", entry)
        print()

        print("-----------------------------------------------------------------")
