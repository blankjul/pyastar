import time
from heapq import heappush, heappop


class Node:

    def __init__(self, key, data=None) -> None:
        super().__init__()
        self.disabled = False
        self.key = key
        self.data = data


class PriorityQueue:

    def __init__(self,
                 func_sorted_by=lambda entry: entry["val"],
                 tie_break="LIFO"
                 ) -> None:

        super().__init__()

        # a priority queue that stores the nodes sorted by the value
        self.pq = []

        # dictionary that maps from each key to the corresponding node object
        self.H = {}

        # counter of how many entries the priority queue currently has
        self.cnt = 0

        # a function that return the value it should be sorted by
        self.func_sorted_by = func_sorted_by

        # how to resolve a tie break - either LIFO or FIFO
        self.tie_break = tie_break

    def push(self, key, entry):

        # implementation is a set. you can not add an element twice.
        if key in self.H:
            raise RuntimeError("You can not add an element twice to this Priority Queue! "
                            "Use replace(entry) if the corresponding values need to be changed.")

        else:
            # create a node object and add it to the map
            node = Node(key, data=entry)
            self.H[key] = node

            # store the timestamp for the tie break
            t = time.time()
            if self.tie_break.upper() == "LIFO":
                t = -t

            val = self.func_sorted_by(entry)
            heappush(self.pq, (val, t, node))

            # increase the counter by one
            self.cnt += 1

            # return the class itself to allow concatenation of pushes
            return self

    def pop(self):

        # until we have found a node that is not disabled
        while True:
            if len(self.pq) == 0:
                raise Exception("Priority Queue is already empty. No element can be returned.")

            # get the node with the lowest value from the priority queue
            val, _, node = heappop(self.pq)

            # if the node is not disabled we are done
            if not node.disabled:
                break

        # because it is popped we remove it from the set and decrease the counter
        del self.H[node.key]
        self.cnt -= 1

        return node.key, node.data

    def remove(self, key):

        # if the entry is currently stored in this data structure
        if key in self.H:
            # disable it to be not returned when popped - it still remains in the pq!
            self.H[key].disabled = True

            # delete from the mapping
            del self.H[key]

            # decrease the counter since it is not stored anymore
            self.cnt -= 1

    def contains(self, key):
        return key in self.H and self.H[key]

    def get(self, key):
        return self.H[key].data

    def size(self):
        return self.cnt

    def empty(self):
        return self.cnt == 0

    def tolist(self, as_tuple=True):
        ret = []
        pq = list(self.pq)
        while len(pq) > 0:
            _, _, node = heappop(pq)
            entry = (node.key, node.data) if as_tuple else node.data
            ret.append(entry)

        return ret
