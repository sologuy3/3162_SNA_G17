import unittest
import pprint

from src.graph.node import Node
from src.graph.graph import Graph

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

    def tearDown(self):
        """Call after every test case."""

    def test_init(self):
        """
        Tests that everything done in the setUp method works correctly.
        """
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(self.graph_a.get_all_edges(stringify=True))
        pp.pprint(self.graph_a.get_all_nodes(stringify=True))


    # todo hasNode
    def test_has_node(self):
        """
        Tests the has_node method.
        This should return true if a graph contains a given node.
        :return: bool
        """
        # basic tests
        # tests whether the graph from setUp had nodes added correctly.
        self.graph_a.has_node(self.node1)

    # todo hasEdge

    # todo addNode

    # todo addEdge

    # todo deleteNode

    # todo deleteEdge

    # todo getNodeNeighbors

    # todo getNodeEdges

    # todo getAllNodes

    # todo getAllEdges

    # todo getWeight


if __name__ == "__main__":
    unittest.main()

