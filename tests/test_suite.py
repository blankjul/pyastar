import os
import sys
import unittest

# add the path to be execute in the main directory
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

testmodules = [
    'tests.test_pq',
    'tests.test_astar',
    # 'tests.test_maze'
]

suite = unittest.TestSuite()
for t in testmodules:
    suite.addTest(unittest.defaultTestLoader.loadTestsFromName(t))

ret = unittest.TextTestRunner().run(suite)

if len(ret.failures) + len(ret.errors) > 0:
    exit(1)
