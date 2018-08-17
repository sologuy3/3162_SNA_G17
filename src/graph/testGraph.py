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


    # def test_add_neighbor_at_init(self):
    #     """Unit test for passing a list of neighbors as an argument when initializing a node'"""
    #     neighbor = Node([self.node_a])
    #     assert neighbor.get_neighbors()[0] is self.node_a, "Neighbor not added"
    #     assert self.node_a.get_neighbors() == [], "Neighbor list should not be updated automatically @Directed"
    #     #todo pass multiple
    #     #todo pass Node instead of list
    #
    # def test_add_neighbors_individual(self):
    #     neighbor = Node()
    #     neighbor.add_neighbor(self.node_a)
    #     assert neighbor.get_neighbors()[0] is self.node_a, "Neighbor not added"
    #     assert self.node_a.get_neighbors() == [], "Neighbor list should not be updated automatically @Directed"
    #
    #     #todo add fail cases
    #
    # def test_add_neighbors_starlist(self):
    #     neighbor_a = Node()
    #     neighbor_a.add_neighbor(*[self.node_a])
    #     assert neighbor_a.get_neighbors()[0] is self.node_a, "Neighbor not added"
    #     assert self.node_a.get_neighbors() == [], "Neighbor list should not be updated automatically @Directed"
    #
    #
    #     #todo pass list
    #     #todo pass tuple
    #     #todo add fail cases
    #     #todo add neighbors with other neighbors


if __name__ == "__main__":
    unittest.main()     # run all tests
