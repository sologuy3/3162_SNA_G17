from src.graph.algorithms import GraphAlgorithms
from src.graph.graph import Graph
from src.graph.node import Node
import unittest
from src.graph import sample_graphs


def initialise_sample_graph(sample_graph):
    graph = Graph(name='SampleGraph')
    for each_node in sample_graph['nodes'].keys():
        graph.add_node(Node(label=each_node))
    for each_edge in sample_graph['weights'].keys():
        node = graph.get_node_from_label(each_edge[0])
        neighbor = graph.get_node_from_label(each_edge[1])
        graph.add_edge(node, neighbor, sample_graph['weights'][each_edge])
    return graph


class BasicGraphTest(unittest.TestCase):
    def setUp(self):
        """Call before every test case."""
        self.basic_graph = Graph(name="myGraph")

        # Simple graph with three nodes
        self.node1 = Node(label='node1')
        self.node2 = Node(label='node2')
        self.node3 = Node(label='node3')

        self.basic_graph.add_node(self.node1)
        self.basic_graph.add_node(self.node2, neighbors={self.node1})
        self.basic_graph.add_node(self.node3, neighbors={self.node1})

        self.graph_algorithms = GraphAlgorithms()

    def tearDown(self):
        """Call after every test case."""

    def test_node_count(self):
        node_count = self.graph_algorithms.node_count(self.basic_graph)
        self.assertEqual(node_count, 3)

    def test_edge_count(self):
        edge_count = self.graph_algorithms.edge_count(self.basic_graph)
        self.assertEqual(edge_count, 2)

    def test_shortest_path(self):
        sample_graph_a = initialise_sample_graph(sample_graphs.graph_a)
        paths = {}
        for source_node in sample_graph_a.get_all_nodes():
            shortest_dist, prev = self.graph_algorithms.shortest_path_length(sample_graph_a, source_node)
            source_label = source_node.label
            length_list = [None] * 5
            for node in shortest_dist.keys():
                # print(source_label+'>'+node.label+':'+str(shortest_dist[node]))
                length_list.__setitem__(int(node.label), shortest_dist[node])
            paths[source_label] = length_list
        # print(paths)
        # print(sample_graphs.graph_a['minpath'])
        self.assertEqual(paths, sample_graphs.graph_a['minpath'])

    def test_average_path(self):
        self.assertEqual(self.graph_algorithms.minimum_average_path(self.basic_graph), 1, "minimum average path failed")
        sample_graph_a = initialise_sample_graph(sample_graphs.graph_a)
        self.assertEqual(self.graph_algorithms.minimum_average_path(sample_graph_a), sample_graphs.graph_a['avgpath'])

    def test_diameter(self):
        self.assertEqual(self.graph_algorithms.diameter(self.basic_graph), 1,
                         'diameter algorithm failed for basic graph')
        sample_graph_a = initialise_sample_graph(sample_graphs.graph_a)
        self.assertEqual(self.graph_algorithms.diameter(sample_graph_a), sample_graphs.graph_a['diameter'],
                         'diameter algorithm failed for sample graph a')
