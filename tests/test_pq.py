import unittest

from pyastar.util.pq import PriorityQueue


class TestPriorityQueue(unittest.TestCase):

    def test_sorting(self):
        pq = PriorityQueue().push(0, 1).push(1, -1).push(2, 0, None)
        self.assertListEqual([-1, 0, 1], [e[1] for e in pq.tolist()])

    def test_add_key_twice_throws_exception(self):
        with self.assertRaises(RuntimeError):
            PriorityQueue().push(0, 1).push(0, -1)

    def test_reinsert_removed_element(self):
        pq = PriorityQueue().push(0, 1).push(1, -1).push(2, 2)
        pq.push(10, 0)
        pq.remove(10)
        pq.push(10, -100)

        key, val, elem = pq.pop()
        self.assertEqual(key, 10)
        self.assertEqual(-100, val)

    def test_lifo(self):
        pq = PriorityQueue().push(0, 1).push(1, 1).push(2, 1)
        self.assertListEqual([2, 1, 0], [key for key, _, _ in pq.tolist()])

    def test_fifo(self):
        pq = PriorityQueue(tie_break="FIFO").push(0, 1).push(1, 1).push(2, 1)
        self.assertListEqual([0, 1, 2], [key for key, _, _ in pq.tolist()])


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
        pq.push(1, (1,2))
        pq.push(2, (1, 3))
        pq.push(3, (1, 2, 1))

        self.assertListEqual([(1,2), (1,2,1), (1,3)], [e[1] for e in pq.tolist()])



if __name__ == '__main__':
    unittest.main()
