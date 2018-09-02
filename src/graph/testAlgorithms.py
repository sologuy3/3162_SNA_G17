from src.graph.algorithms import GraphAlgorithms
from src.graph.graph import Graph
from src.graph.node import Node
import unittest
from  src.graph import sample_graphs

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


    def initialise_sample_graph(self,sample_graph):
        graph = Graph(name='SampleGraph')
        for each_node in sample_graph['nodes'].keys():
            graph.add_node(Node(label=each_node))
        for each_edge in sample_graph['weights'].keys():
            node = graph.get_node_from_label(each_edge[0])
            neighbor = graph.get_node_from_label(each_edge[1])
            graph.add_edge(node,neighbor,sample_graph['weights'][each_edge])
        return graph


    def test_node_count(self):
        node_count = self.graph_algorithms.node_count(self.graph_a)
        self.assertEqual(node_count, 3)

    def test_edge_count(self):
        edge_count = self.graph_algorithms.edge_count(self.graph_a)
        self.assertEqual(edge_count, 2)

    def test_shortest_path(self):
        shortest_path_node1 = self.graph_algorithms.shortest_path_length(self.graph_a, self.node2)
        sample_graph_a = self.initialise_sample_graph(sample_graphs.graph_a)
        for each_node in sample_graph_a.get_all_nodes():
            shortest_dist, prev = self.graph_algorithms.shortest_path_length(sample_graph_a,each_node)
            source = each_node.label
            # todo finish writing test

    def test_average_path(self):
        self.assertEqual(self.graph_algorithms.minimum_average_path(self.graph_a),1,"minimum average path failed")
        print(self.graph_algorithms.minimum_average_path(self.initialise_sample_graph(sample_graphs.graph_a)))