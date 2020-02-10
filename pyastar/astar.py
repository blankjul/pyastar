from pyastar.problem import Problem
from pyastar.util.node import NodeFactory
from pyastar.util.pq import PriorityQueueSet


class AStar:

    def __init__(self,
                 problem,
                 heuristic_is_inconsistent=False,
                 open_set_max_size=None,
                 open_set_truncate_size=None,
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

        # initialize the open set as custom priority queue (implemented as a set)
        self.open_set = PriorityQueueSet()

        # the maximum size of the open set - if it is not None what is the size it should be truncated to
        self.open_set_max_size = open_set_max_size
        self.open_set_truncate_size = open_set_truncate_size

        # keep track of all nodes that are already closed
        self.closed_set = {}

        # assuming the heuristic is inconsistent we change the behavior slightly
        self.heuristic_is_inconsistent = heuristic_is_inconsistent
        if self.heuristic_is_inconsistent:
            self.pop = self.pop_if_inconsistent
            self.skip = self.skip_if_inconsistent

    def find(self, **kwargs):
        self.initialize()
        while self.has_next():
            self.next()
        return self.result(**kwargs)

    def initialize(self):
        self.add(self.factory.create())
        return self

    def next(self):
        # retrieve the first node and remove it
        self.pop()

        # if pop was successful
        if self.node is not None:

            # if the verbose flag is set to true, print some information about the current status
            if self.verbose:
                self.info()

            # actually process the node
            self.process()

            # does the truncation of the open queue if it is enabled - otherwise nothing happens
            self.truncate_if_necessary()

    def process(self):
        # get access to the current node directly
        node = self.node

        # if the verbose flag is set to true, print some information about the current status
        if self.verbose:
            self.info()

        # mark this key to be visited by adding it to the closed set
        self.closed_set[node.key] = node

        # if the goal has been found - we know it is optimal if the heuristic is admissible
        if node.is_goal():
            self.goal_found()
        else:

            for neighbor in node.get_neighbors():

                neighbor = self.factory.create(neighbor)
                neighbor.set_previous(node)

                # if the node is not supposed to be skipped
                if not self.skip(neighbor):
                    self.add(neighbor)

    def add(self, node):

        # if we have been there - remove it from the priority queue because we have found a better one
        self.open_set.remove(node.key)

        # create a new entry containing the necessary information
        node.calc_g_h_f()

        # finally add to the open set
        self.open_set.push(node.key, node.f, node)

        return True

    def has_next(self):
        # if there are no nodes to process the algorithm always terminates
        if self.open_set.empty():
            return False
        else:
            return self.opt is None

    def goal_found(self):
        self.opt = {"path": reconstruct_path(self.node), "node": self.node, "costs": self.node.g}

    def pop(self):
        self.node = self.open_set.pop()

    def truncate_if_necessary(self):
        if self.open_set_max_size is not None and self.open_set.size() > self.open_set_max_size:
            if self.open_set_truncate_size is None:
                raise Exception("Please set open_set_truncate_size if you have enabled a maximum size!")
            else:
                return self.truncate()

    def truncate(self):
        if self.open_set_max_size is not None and self.open_set.size() > self.open_set_max_size:
            _node = self.node

            pq = PriorityQueueSet()
            while self.open_set.size() > 0 and pq.size() < self.open_set_truncate_size:
                self.pop()
                n = self.node
                pq.push(n.key, n.f, n)

            self.open_set = pq
            self.node = _node

    def skip(self, node):
        if node.key in self.closed_set:
            return True
        else:
            if not self.open_set.contains(node.key):
                return False
            else:
                node.calc_g()
                node_in_open_set = self.open_set.get(node.key)
                return node_in_open_set.g <= node.g

    def skip_if_inconsistent(self, node):
        if node.key in self.closed_set:
            node.calc_g()
            node_in_closed_set = self.closed_set[node.key]
            return node_in_closed_set.g <= node.g
        else:
            if not self.open_set.contains(node.key):
                return False
            else:
                node.calc_g()
                node_in_open_set = self.open_set.get(node.key)
                return node_in_open_set.g <= node.g

    def pop_if_inconsistent(self):
        self.node = None
        while not self.open_set.empty():
            node = self.open_set.pop()
            if not self.skip_if_inconsistent(node):
                self.node = node
                break

    def result(self, **kwargs):
        return extract(self.opt, **kwargs)

    def info(self):
        from copy import deepcopy
        _node, _open = self.node, deepcopy(self.open_set)

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
