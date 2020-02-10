import unittest

from pyastar.util.pq import PriorityQueueSet as PriorityQueue


class TestPriorityQueue(unittest.TestCase):

    def test_sorting(self):
        pq = PriorityQueue().push(0, 1).push(1, -1).push(2, 0, None)
        self.assertListEqual([-1, 0, 1], [e for e in pq.tolist(return_value=True, return_obj=False)])

    def test_add_key_twice_throws_exception(self):
        with self.assertRaises(RuntimeError):
            PriorityQueue().push(0, 1).push(0, -1)

    def test_reinsert_removed_element(self):
        pq = PriorityQueue().push(0, 1).push(1, -1).push(2, 2)
        pq.push(10, 0)
        pq.remove(10)
        pq.push(10, -100)

        key, val = pq.pop(return_key=True, return_value=True, return_obj=False)
        self.assertEqual(key, 10)
        self.assertEqual(-100, val)

    def test_lifo(self):
        pq = PriorityQueue().push(0, 1).push(1, 1).push(2, 1)
        self.assertListEqual([2, 1, 0], [key for key  in pq.tolist(return_key=True, return_obj=False)])

    def test_fifo(self):
        pq = PriorityQueue(tie_break="FIFO").push(0, 1).push(1, 1).push(2, 1)
        self.assertListEqual([0, 1, 2], [key for key in pq.tolist(return_key=True, return_obj=False)])

    def test_size(self):
        pq = PriorityQueue()
        self.assertEqual(0, pq.size())

        pq.push(0, 0)
        self.assertEqual(1, pq.size())

        pq.push(1, 1)
        self.assertEqual(2, pq.size())

        pq.remove(1)
        self.assertEqual(1, pq.size())

        pq.push(1, 1)
        self.assertEqual(2, pq.size())

    def test_multiple_sorting_criteria(self):
        pq = PriorityQueue()
        pq.push(1, (1, 2))
        pq.push(2, (1, 3))
        pq.push(3, (1, 2, 1))

        self.assertListEqual([(1, 2), (1, 2, 1), (1, 3)], [e for e in pq.tolist(return_value=True, return_obj=False)])

    def test_free_memory_ratio(self):
        pq = PriorityQueue(free_memory_min_entries=0)
        pq.push(1, (1, 2))
        pq.push(2, (1, 3))
        pq.push(3, (1, 2, 1))
        pq.push(4, (1, 2, 1))
        pq.push(5, (1, 2, 1))

        pq.remove(1)
        self.assertEqual(5, len(pq.pq))

        pq.remove(2)
        self.assertEqual(3, len(pq.pq))



if __name__ == '__main__':
    unittest.main()
