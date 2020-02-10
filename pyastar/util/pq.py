import time
from heapq import heappush, heappop


class Entry:

    def __init__(self, key, value, obj=None) -> None:
        super().__init__()
        self.key = key
        self.value = value
        self.obj = obj
        self.disabled = False


class PriorityQueueSet:

    def __init__(self,
                 tie_break="LIFO",
                 free_memory_ratio=0.75,
                 free_memory_min_entries=200) -> None:

        super().__init__()

        # a priority queue that stores the nodes sorted by the value
        self.pq = []

        # dictionary that maps from each key to the corresponding node object
        self.H = {}

        # counter of how many entries the priority queue currently has
        self.cnt = 0

        # how to resolve a tie break - either LIFO or FIFO
        self.tie_break = tie_break

        # the ratio in the pq when the memory is freed
        self.free_memory_ratio = free_memory_ratio

        # minimum number of entries until the memory is freed
        self.free_memory_min_entries = free_memory_min_entries

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
                return None

            # get the node with the lowest value from the priority queue
            node = heappop(self.pq)[-1]

            # if the node is not disabled we are done
            if not node.disabled:
                break

        # because it is popped we remove it from the set and decrease the counter
        del self.H[node.key]
        self.cnt -= 1

        return return_element(node, **kwargs)

    def remove(self, key):

        # if the entry is currently stored in this data structure
        if key in self.H:

            # disable it to be not returned when popped - it still remains in the pq!
            self.H[key].disabled = True

            # delete from the mapping
            del self.H[key]

            # decrease the counter since it is not stored anymore
            self.cnt -= 1

            # see if the memory should be freed or not
            if len(self.pq) >= self.free_memory_min_entries and self.cnt / len(self.pq) < self.free_memory_ratio:
                self.free_memory()

    def contains(self, key):
        return key in self.H and self.H[key]

    def get(self, key):
        return self.H[key].obj

    def size(self):
        return self.cnt

    def empty(self):
        return self.cnt == 0

    def free_memory(self):
        pq = []
        while len(self.pq) > 0:
            t = heappop(self.pq)
            entry = t[-1]
            if not entry.disabled:
                heappush(pq, t)
        self.pq = pq

    def tolist(self, **kwargs):
        ret = []
        pq = list(self.pq)
        while len(pq) > 0:
            node = heappop(pq)[-1]
            entry = return_element(node, **kwargs)
            ret.append(entry)

        return ret


def return_element(node, return_key=False, return_value=False, return_obj=True):
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


class PriorityQueue:

    def __init__(self,
                 tie_break="LIFO") -> None:

        super().__init__()

        # a priority queue that stores the nodes sorted by the value
        self.pq = []

        # counter of how many entries the priority queue currently has
        self.cnt = 0

        # how to resolve a tie break - either LIFO or FIFO
        self.tie_break = tie_break

    def push(self, value, obj=None):

        # create a node object and add it to the map
        node = Entry(None, value, obj=obj)

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

        # get the node with the lowest value from the priority queue
        node = heappop(self.pq)[-1]

        # because it is popped we remove it from the set and decrease the counter
        self.cnt -= 1

        return return_element(node, **kwargs)

    def size(self):
        return self.cnt

    def empty(self):
        return self.cnt == 0

    def tolist(self, **kwargs):
        ret = []
        pq = list(self.pq)
        while len(pq) > 0:
            node = heappop(pq)[-1]
            entry = return_element(node, **kwargs)
            ret.append(entry)

        return ret
