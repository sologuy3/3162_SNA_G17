import unittest
from graph import Graph

class NodeTest(unittest.TestCase):
    def setUp(self):
        """Call before every test case."""
        self.test_graph = Graph()

    def tearDown(self):
        """Call after every test case."""
