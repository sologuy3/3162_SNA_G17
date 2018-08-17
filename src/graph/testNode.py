import unittest
from src.graph.node import Node

class NodeTest(unittest.TestCase):
    def setUp(self):
        """Call before every test case."""
        self.node_a = Node()

    def tearDown(self):
        """Call after every test case."""

    def test_add_neighbor_at_init(self):
        """Unit test for passing a list of neighbors as an argument when initializing a node'"""
        neighbor = Node([self.node_a]) # initialise a new node to use for this test
        # Make sure the added node is accessible through the get method
        self.assertIs(neighbor.get_neighbors().pop(),self.node_a, "Neighbor not added")
        # Make sure the neighbor is not automatically updated
        self.assertEqual(self.node_a.get_neighbors(), set(), "Neighbor list should not be updated automatically @Directed")
        # Make sure passing a Node instead of a list is handled correctly
        with self.assertRaises(AssertionError):
             Node(neighbor)

    def test_add_neighbors_at_init(self):
        neighbor_list = set()
        for _ in range(2):
            neighbor_list.add(Node())
        many_node = Node(neighbor_list)
        self.assertEqual(many_node.get_neighbors(),neighbor_list,"Passing a large Neighbor list at Node Init fails")


        #todo pass multiple
        #todo pass Node instead of list

    def test_add_neighbors_individual(self):
        neighbor = Node()
        neighbor.add_neighbor(self.node_a)
        assert neighbor.get_neighbors().pop() is self.node_a, "Neighbor not added"
        assert self.node_a.get_neighbors() == set(), "Neighbor list should not be updated automatically @Directed"

        #todo add fail cases

    def test_add_neighbors_starlist(self):
        neighbor_a = Node()
        neighbor_a.add_neighbor(*[self.node_a])
        assert neighbor_a.get_neighbors().pop() is self.node_a, "Neighbor not added"
        assert self.node_a.get_neighbors() == set(), "Neighbor list should not be updated automatically @Directed"


        #todo pass list
        #todo pass tuple
        #todo add fail cases
        #todo add neighbors with other neighbors


if __name__ == "__main__":
    unittest.main()     # run all tests
