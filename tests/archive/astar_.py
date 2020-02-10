from pyastar.problem import Problem
from pyastar.util.node import NodeFactory
from pyastar.util.pq import PriorityQueue


class AStar:

    def __init__(self,
                 problem,
                 revisit_if_inconsistent=False,
                 verbose=False,
                 ):

        # either the user provides the problem or directly a node factory (allows more customization)
        if isinstance(problem, Problem):
            self.factory = NodeFactory(problem)
        else:
            self.factory = problem

        # whether printout in each iteration is desired
        self.verbose = verbose

        # the optimal path to be returned
        self.opt = None

        # the current node that is processed
        self.node = None

        # all nodes that have been added during the last next call
        self.added = None

        # initialize the open set as custom priority queue (implemented as a set)
        self.pq = PriorityQueue()

        # store nodes that are already closed
        self.closed = {}

    def find(self, **kwargs):
        self.initialize()
        while self.has_next():
            self.next()
        return self.result(**kwargs)

    def initialize(self):
        node = self.factory.create()
        node.calc_g()
        node.calc_h()
        node.calc_f()
        self.pq.push(node.f, node)
        return self

    def next(self):

        # if an element could be popped and is set to current
        if self.pop():

            # get the current information of the key
            node = self.node

            # get access to the open and closed set
            _open, _closed = self.pq, self.closed

            # if the verbose flag is set to true, print some information about the current status
            if self.verbose:
                self.info()

            # mark this key to be visited by adding it to the closed set
            self.closed[node.key] = node

            # if the goal has been found - we know it is optimal if the heuristic is admissible
            if node.is_goal():
                self.goal_found()
            else:
                # reset the key that has been extended in the last step
                self.added = []

                for neighbor in node.get_neighbors():
                    neighbor = self.factory.create(neighbor)
                    neighbor.set_previous(node)
                    is_better = self.is_node_better(neighbor)

                    if is_better:
                        self.add(neighbor)
                        self.added.append(neighbor)

    def add(self, neighbor):
        _node, _open = self.node, self.pq

        # if we have been there - remove it from the priority queue because we have found a better one
        if _open.contains(neighbor.key):
            _open.remove(neighbor.key)

        # create a new entry containing the necessary information
        neighbor.calc_h()
        neighbor.calc_f()

        # and store the new improved entry
        _open.push(neighbor.key, neighbor.f, neighbor)

    def has_next(self):
        # if there are no nodes to process the algorithm always terminates
        if self.pq.empty():
            return False
        else:
            return self.opt is None

    def skip(self, node):
        return False

    def goal_found(self):
        self.opt = {"path": reconstruct_path(self.node), "node": self.node, "costs": self.node.g}

    def pop(self):
        _open, _closed = self.pq, self.closed

        # initially set the current value to non - to check if something was set or not
        self.node = None

        # pop the first element - if heuristic is inconsistent we might skip nodes that have be revisited
        if not self.revisit_if_inconsistent:
            self.node = _open.pop(return_key=False, return_value=False)

        else:
            while not _open.empty():
                node = _open.pop(return_key=False, return_value=False)

                # either take a node if not in closed at all or if the closed not was not better or equally good than it
                if node not in _closed or node.g < _closed[node].g:
                    self.node = node
                    break

        return self.node is not None

    def is_node_better(self, neighbor):
        prev, _open, _closed = self.node, self.pq, self.closed

        # the following code snippets decides whether the node should be added to the open set or not
        if neighbor.key in _closed:

            # if the heuristic is consistent a node is visited only once - therefore it can not be improved
            if not self.revisit_if_inconsistent:
                is_better = False

            # if inconsistent and the flag is activated check whether we have improved compared to a closed node
            else:
                neighbor.calc_g(prev)
                is_better = neighbor.g < _closed[neighbor.key].g

        # if a node has never been visited yet
        else:
            neighbor.calc_g()

            if not _open.contains(neighbor.key):
                is_better = True
            else:
                is_better = neighbor.g < _open.get(neighbor.key).g

        return is_better

    def result(self, **kwargs):
        return extract(self.opt, **kwargs)

    def info(self):
        from copy import deepcopy
        _node, _open = self.node, deepcopy(self.pq)

        print("CURRENT")
        print(_node.key, "->", _node.__dict__)
        print()

        print("OPEN SET")
        for k in range(min(10, _open.size())):
            entry = _open.pop()
            print(entry.key, "->", entry.__dict__)
        print()

        print("-----------------------------------------------------------------")


def extract(opt, return_path=True, return_costs=True, return_node=False):
    ret = []
    if return_path:
        ret.append(opt["path"])
    if return_costs:
        ret.append(opt["costs"])
    if return_node:
        ret.append(opt["node"])
    return tuple(ret)


def reconstruct_path(node):
    path = []
    while node.prev is not None:
        path.append(node.key)
        node = node.prev
    path.append(node.key)
    return tuple(path[::-1])


def evaluate_path(problem, path):
    costs = 0
    for k in range(len(path) - 1):
        costs += problem.get_costs(path[k], path[k + 1])
    return costs
