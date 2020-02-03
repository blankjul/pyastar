import time
from heapq import heappush, heappop


class Entry:

    def __init__(self, key, value, obj=None) -> None:
        super().__init__()
        self.disabled = False
        self.key = key
        self.value = value
        self.obj = obj


class PriorityQueue:

    def __init__(self, tie_break="LIFO") -> None:

        super().__init__()

        # a priority queue that stores the nodes sorted by the value
        self.pq = []

        # dictionary that maps from each key to the corresponding node object
        self.H = {}

        # counter of how many entries the priority queue currently has
        self.cnt = 0

        # how to resolve a tie break - either LIFO or FIFO
        self.tie_break = tie_break

    def push(self, key, value, obj=None):

        # implementation is a set. you can not add an element twice.
        if key in self.H:
            raise RuntimeError("You can not add an element twice to this Priority Queue! "
                               "Use replace(entry) if the corresponding values need to be changed.")

        else:
            # create a node object and add it to the map
            node = Entry(key, value, obj=obj)
            self.H[key] = node

            # store the timestamp for the tie break
            t = time.time()
            if self.tie_break.upper() == "LIFO":
                t = -t

            # make sure value is an actual list
            if isinstance(value, tuple):
                value = list(value)
            elif not isinstance(value, list):
                value = [value]

            heappush(self.pq, tuple(value + [t, node]))

            # increase the counter by one
            self.cnt += 1

            # return the class itself to allow concatenation of pushes
            return self

    def pop(self, **kwargs):

        # until we have found a node that is not disabled
        while True:
            if len(self.pq) == 0:
                raise Exception("Priority Queue is already empty. No element can be returned.")

            # get the node with the lowest value from the priority queue
            node = heappop(self.pq)[-1]

            # if the node is not disabled we are done
            if not node.disabled:
                break

        # because it is popped we remove it from the set and decrease the counter
        del self.H[node.key]
        self.cnt -= 1

        return self._return_element(node, **kwargs)

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
        return self.H[key].obj

    def size(self):
        return self.cnt

    def empty(self):
        return self.cnt == 0

    def _return_element(self, node, return_key=True, return_value=True, return_obj=True):
        ret = []
        if return_key:
            ret.append(node.key)
        if return_value:
            ret.append(node.value)
        if return_obj:
            ret.append(node.obj)

        if len(ret) == 1:
            return ret[0]
        else:
            return tuple(ret)

    def tolist(self, **kwargs):
        ret = []
        pq = list(self.pq)
        while len(pq) > 0:
            node = heappop(pq)[-1]
            entry = self._return_element(node, **kwargs)
            ret.append(entry)

        return ret
