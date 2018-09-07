import unittest

from sna.graph.graph import Graph
from sna.graph.node import Node


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
        This test includes
        - Confirming that the internal graph of form {<node1>:{<neighbor1>,<neighbor2>},...} is updated
        - Confirming that the internal weights of form {(<node1>,<node2>):weight),...} is updated
        - Confirming node.neighbors is updated.
        - Confirming that node.neighbors and node.weights always reflect each other.
        """
        self.assertEqual(len(self.graph_a._graph), 3, "Node seems to be missing from _graph")
        self.assertEqual(len(self.graph_a._weights), 2, "Weight seems to be missing from _weights ")

        self.assertEqual(self.node2.get_neighbors(), {self.node1},
                         "Neighbor doesn't seem to be added at the node level")
        self.assertEqual(self.node3.get_neighbors(), {self.node1},
                         "Neighbor doesn't seem to be added at the node level")

        for node in self.graph_a._graph.keys():
            neighbors = node.get_neighbors()
            if neighbors:
                for neighbor in neighbors:
                    self.assertIn((node, neighbor), self.graph_a._weights,
                                  "Weights don't seem to have updated correctly")

    def test_has_node(self):
        """
        Test the has_node() method.
        The expectation is that passing any node that has been added to the graph returns True.
        :return:
        """

        # hasNode successful cases
        self.assertTrue(self.graph_a.has_node(self.node1), "has_node() returning False when it should not")
        self.assertTrue(self.graph_a.has_node(self.node2), "has_node() returning False when it should not")
        self.assertTrue(self.graph_a.has_node(self.node3), "has_node() returning False when it should not")

        # hasNode failure cases
        fail_node1 = Node()

        # node that has been added as a neighbor outside of the graph
        fail_neighbor = Node()
        fail_node2 = Node(neighbors={fail_neighbor})
        self.graph_a.add_node(fail_node2)

        # make sure node that has not been added returns false
        self.assertFalse(self.graph_a.has_node(fail_node1),
                         "has_node() returns True for a node that has not been added")

        self.assertTrue(self.graph_a.has_node(fail_node2), "has_node() returning False when it should not")
        error_msg = "Returns True for node that has been added as a neighbor outside of the graph"
        self.assertFalse(self.graph_a.has_node(fail_neighbor), error_msg)

    def test_has_edge(self):
        """
        Tests the has_edge method.
        The expectation is that passing any edge (directed) that has been added to the graph returns True.
        - Tests that the function returns True when expected
        - Tests that the function returns False when expected
        - Tests that the function raises an exception when either of the nodes are not in the graph
        :return:
        """

        # hasEdge successful cases
        self.assertTrue(self.graph_a.has_edge(self.node2, self.node1), "has_edge() returning False when it should not")
        self.assertTrue(self.graph_a.has_edge(self.node3, self.node1), "has_edge() returning False when it should not")

        # hasEdge fail cases
        self.assertFalse(self.graph_a.has_edge(self.node1, self.node2), "has_edge() returning True when it should not")
        self.assertFalse(self.graph_a.has_edge(self.node1, self.node3), "has_edge() returning True when it should not")
        self.assertFalse(self.graph_a.has_edge(self.node3, self.node3),
                         "has_edge() returning True for not-added self-edge")

        self.assertRaises(AssertionError, self.graph_a.has_edge, self.node1, Node())
        self.assertRaises(AssertionError, self.graph_a.has_edge, Node(), self.node1)
        self.assertRaises(AssertionError, self.graph_a.has_edge, self.node2, Node({self.node2}))

        fail_node1 = Node()
        fail_neighbor = Node({fail_node1})
        self.assertRaises(AssertionError, self.graph_a.has_edge, fail_node1, fail_neighbor)
        self.assertRaises(AssertionError, self.graph_a.has_edge, fail_neighbor, fail_node1)

    def test_add_node(self):
        """
        Tests the add_node() method
        :return:
        """
        # true cases
        self.assertIn(self.node1, self.graph_a._graph, "has_node failed to add nodes")
        self.assertIn(self.node2, self.graph_a._graph, "has_node failed to add nodes")
        self.assertIn(self.node3, self.graph_a._graph, "has_node failed to add nodes")

        # fail cases
        node4 = Node()
        node5 = Node()
        # incorrectly passed node
        self.assertRaises(AssertionError,self.graph_a.add_node,(node4,node5))
        self.assertRaises(AssertionError,self.graph_a.add_node,None)
        # incorrectly passed neighbors
        self.assertRaises(AssertionError,self.graph_a.add_node,node4,node5)
        self.assertRaises(AssertionError,self.graph_a.add_node,node5,node5)

    def test_add_edge(self):
        """
        Tests adding edges between two existing nodes using the add_edge() method
        :return:
        """
        # generic/correct use
        self.graph_a.add_edge(self.node2,self.node3)
        self.assertIn((self.node2,self.node3),self.graph_a._weights)    # tests that it was added to weights
        self.assertIn(self.node3,self.graph_a._graph[self.node2])       # tests that it was added to _graph
        # adding multiple edges
        neighbor_list = []
        for _ in range(1):
            temp_node = Node()
            neighbor_list.append(temp_node)
            self.graph_a.add_node(temp_node)
            self.graph_a.add_edge(self.node3,temp_node)

        for neighbor in neighbor_list:
            self.assertIn((self.node3, neighbor), self.graph_a._weights.keys())  # tests that it was added to weights
            self.assertIn(neighbor, self.graph_a._graph[self.node3])  # tests that it was added to _graph

        # add a -> b and b -> a
        for neighbor in neighbor_list:
            self.graph_a.add_edge(neighbor, self.node3)

        for neighbor in neighbor_list:
            self.assertIn((neighbor, self.node3), self.graph_a._weights.keys())  # tests that it was added to weights
            self.assertIn(self.node3, self.graph_a._graph[neighbor])  # tests that it was added to _graph

    # todo deleteNode
    def test_delete_node(self):
        """ test the delete_node method"""
        self.graph_a.add_edge(self.node1, self.node3)
        self.assertIn((self.node1,self.node3), self.graph_a._weights)
        self.assertIn((self.node3,self.node1), self.graph_a._weights)

        self.assertTrue(self.graph_a.has_node(self.node1))

        self.graph_a.delete_node(self.node1)

        print(self.graph_a.get_all_edges(stringify=True))

        self.assertFalse(self.graph_a.has_node(self.node1))

        # confirm that the internal methods for clearing out the relationships were successful
        self.assertNotIn((self.node1,self.node3), self.graph_a._weights)
        self.assertNotIn((self.node3,self.node1), self.graph_a._weights)
        self.assertRaises(KeyError,self.graph_a._graph.__getitem__,self.node1)

        # confirm _graph neighbors have been deleted

        for node, neighbors in self.graph_a._graph.items():
            print(self.node1, "|||", node)
            self.assertNotIn(self.node1,neighbors)

        self.assertNotIn(self.node1,self.graph_a._graph.keys())

    def test_incoming_node_neighbors(self):
        self.assertEqual(self.graph_a.get_incoming_neighbors(self.node1),{self.node2,self.node3})

    # todo deleteEdge

    # todo getNodeNeighbors

    # todo getNodeEdges

    # todo getAllNodes

    # todo getAllEdges

    # todo getWeight


if __name__ == "__main__":
    unittest.main()

