from graph_sna.graph.algorithms import GraphAlgorithms
from graph_sna.graph.graph import Graph
from graph_sna.graph.graph import Node
import unittest
from graph_sna.graph import sample_graphs


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
        sample_graph_a = initialise_sample_graph(sample_graphs.graph_a)
        self.assertEqual(self.graph_algorithms.node_count(sample_graph_a),5)


    def test_edge_count(self):
        edge_count = self.graph_algorithms.edge_count(self.basic_graph)
        self.assertEqual(edge_count, 2)
        sample_graph_a = initialise_sample_graph(sample_graphs.graph_a)
        self.assertEqual(self.graph_algorithms.edge_count(sample_graph_a),5)


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

    def test_mode_path(self):
        self.assertEqual(self.graph_algorithms.mode_path_length(self.basic_graph), (1, 2),
                         'mode_path_length algorithm failed for basic graph')
        sample_graph_a = initialise_sample_graph(sample_graphs.graph_a)
        self.assertEqual(self.graph_algorithms.mode_path_length(sample_graph_a), sample_graphs.graph_a['mode_path_length'],
                         'mode_path_length algorithm failed for sample graph a')

    def test_median_path(self):
        self.assertEqual(self.graph_algorithms.median_path_length(self.basic_graph), 1,
                         'median_path_length algorithm failed for basic graph')
        sample_graph_a = initialise_sample_graph(sample_graphs.graph_a)
        self.assertEqual(self.graph_algorithms.median_path_length(sample_graph_a),
                         sample_graphs.graph_a['median_path_length'],
                         'median_path_length algorithm failed for sample graph a')

    def test_average_edges_per_node(self):
        self.assertEqual(self.graph_algorithms.average_edges_per_node(self.basic_graph),0.67,
                         'average_edges_per_node algorithm failed for sample graph a')
        sample_graph_a = initialise_sample_graph(sample_graphs.graph_a)
        self.assertEqual(self.graph_algorithms.average_edges_per_node(sample_graph_a),1.0,
                         'average_edges_per_node algorithm failed for sample graph a')

    def test_dfs(self):     # todo finish test_dfs
        print(self.graph_algorithms.depth_first_search(self.basic_graph,self.node1))

    def test_discover_components(self):      # todo finish test_clustering
        sample_graph_b = initialise_sample_graph(sample_graphs.graph_b)
        print(self.graph_algorithms.discover_components(sample_graph_b))

    def test_edmonds(self):
        sample_graph_c = initialise_sample_graph(sample_graphs.graph_c)
        source = sample_graph_c.get_node_from_label('0')
        sink = sample_graph_c.get_node_from_label('11')
        print(self.graph_algorithms.edmonds_karp(sample_graph_c,source,sink))

    def test_local_clustering_coefficient(self):
        print(self.graph_algorithms.local_clustering_coefficient(self.basic_graph,self.node1))

    def test_global_clustering_coefficient(self):
        print(self.graph_algorithms.average_clustering_coefficient(self.basic_graph))

    def test_save_graph_agls(self):
        test_graph = Graph('test')
        test_graph.load_save(self.basic_graph.get_save())
        print(self.graph_algorithms.node_count(test_graph))

    def test_structural_holes(self):
        sample_graph_c = initialise_sample_graph(sample_graphs.graph_c)

        print(sample_graph_c.get_save())
        print(self.graph_algorithms.structural_holes(sample_graph_c))
