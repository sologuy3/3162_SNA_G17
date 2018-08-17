import unittest

from src.graph.node import Node
from src.graph.graph import Graph

class GraphTest(unittest.TestCase):
    def setUp(self):
        """Call before every test case."""
        self.graph_a = Graph(name="myGraph")

        # Simple graph with three nodes
        node1 = Node()
        node2 = Node()
        node3 = Node()

        self.graph_a.add_nodes(node1)
        self.graph_a.add_nodes(node2, neighbors={node1})
        self.graph_a.add_nodes(node3, neighbors={node1})

    def tearDown(self):
        """Call after every test case."""