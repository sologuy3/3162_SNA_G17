from src.graph.algorithms import GraphAlgorithms
from src.graph.graph import Graph
from src.graph.node import Node
import unittest


class BasicGraphTest(unittest.TestCase):
    def setUp(self):
        """Call before every test case."""
        self.graph_a = Graph(name="myGraph")

        # Simple graph with three nodes
        self.node1 = Node(label='node1')
        self.node2 = Node(label='node2')
        self.node3 = Node(label='node3')

        self.graph_a.add_node(self.node1)
        self.graph_a.add_node(self.node2, neighbors={self.node1})
        self.graph_a.add_node(self.node3, neighbors={self.node1})

        self.graph_algorithms = GraphAlgorithms()

    def tearDown(self):
        """Call after every test case."""

    def test_node_count(self):
        node_count = self.graph_algorithms.node_count(self.graph_a)
        self.assertEqual(node_count, 3)

    def test_edge_count(self):
        edge_count = self.graph_algorithms.edge_count(self.graph_a)
        self.assertEqual(edge_count, 2)

    def test_shortest_path(self):
        shortest_path_node1 = self.graph_algorithms.shortest_path_length(self.graph_a, self.node2)
        print(shortest_path_node1)
