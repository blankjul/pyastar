import unittest

from pyastar.util.pq import PriorityQueue


class TestPriorityQueue(unittest.TestCase):

    def test_sorting(self):
        pq = PriorityQueue().push(0, {"val": 1}).push(1, {"val": -1}).push(2, {"val": 0})
        self.assertListEqual([-1, 0, 1], [e["val"] for e in pq.tolist(as_tuple=False)])

    def test_sorting_custom(self):
        pq = PriorityQueue(func_sorted_by=lambda x: x["f"]).push(0, {"f": 1}).push(1, {"f": -1}).push(2, {"f": 0})
        self.assertListEqual([-1, 0, 1], [e["f"] for e in pq.tolist(as_tuple=False)])

    def test_add_key_twice_throws_exception(self):
        with self.assertRaises(RuntimeError):
            PriorityQueue().push(0, {"val": 1}).push(0, {"val": -1})

    def test_reinsert_removed_element(self):
        pq = PriorityQueue().push(0, {"val": 1}).push(1, {"val": -1}).push(2, {"val": 0})
        pq.push(10, {"val": 0})
        pq.remove(10)
        pq.push(10, {"val": -100})

        key, elem = pq.pop()
        self.assertEqual(key, 10)
        self.assertEqual(-100, elem["val"])

    def test_lifo(self):
        pq = PriorityQueue().push(0, {"val": 1}).push(1, {"val": 1}).push(2, {"val": 1})
        self.assertListEqual([2, 1, 0], [key for key, _ in pq.tolist()])

    def test_fifo(self):
        pq = PriorityQueue(tie_break="FIFO").push(0, {"val": 1}).push(1, {"val": 1}).push(2, {"val": 1})
        self.assertListEqual([0, 1, 2], [key for key, _ in pq.tolist()])


    def test_size(self):
        pq = PriorityQueue()
        self.assertEqual(0, pq.size())

        pq.push(0, {"val": 0})
        self.assertEqual(1, pq.size())

        pq.push(1, {"val": 1})
        self.assertEqual(2, pq.size())

        pq.remove(1)
        self.assertEqual(1, pq.size())

        pq.push(1, {"val": 1})
        self.assertEqual(2, pq.size())


if __name__ == '__main__':
    unittest.main()
