import unittest
from node import Node

class NodeTest(unittest.TestCase):
    def setUp(self):
        """Call before every test case."""
        self.node_a = Node()

    def tearDown(self):
        """Call after every test case."""

    def test_add_neighbor_at_init(self):
        """Unit test for passing a list of neighbors as an argument when initializing a node'"""
        neighbor = Node([self.node_a])
        assert neighbor.get_neighbors()[0] is self.node_a, "Neighbor not added"
        assert self.node_a.get_neighbors() == [], "Neighbor list should not be updated automatically @Directed"
        #todo pass multiple
        #todo pass Node instead of list

    def test_add_neighbors_individual(self):
        neighbor = Node()
        neighbor.add_neighbor(self.node_a)
        assert neighbor.get_neighbors()[0] is self.node_a, "Neighbor not added"
        assert self.node_a.get_neighbors() == [], "Neighbor list should not be updated automatically @Directed"

        #todo add fail cases

    def test_add_neighbors_starlist(self):
        neighbor_a = Node()
        neighbor_a.add_neighbor(*[self.node_a])
        assert neighbor_a.get_neighbors()[0] is self.node_a, "Neighbor not added"
        assert self.node_a.get_neighbors() == [], "Neighbor list should not be updated automatically @Directed"


        #todo pass list
        #todo pass tuple
        #todo add fail cases
        #todo add neighbors with other neighbors


if __name__ == "__main__":
    unittest.main()     # run all tests
