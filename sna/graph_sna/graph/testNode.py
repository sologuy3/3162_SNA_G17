import gc
import unittest

from graph_sna.graph.node import Node


class NodeTest(unittest.TestCase):
    def setUp(self):
        """Call before every test case."""
        self.node_a = Node()

    def tearDown(self):
        """Call after every test case."""
        gc.collect()

    def test_add_neighbor_at_init(self):
        """
        Test for passing a one neighbor as an argument when initializing a node.
        Fails if added neighbor:
        - Is not returned in node.get_neighbors()
        - Has the new node added to its neighbor list automatically (i.e. non-directed edges)
        """
        neighbor = Node([self.node_a])  # initialise a new node to use for this test
        # Make sure the added node is accessible through the get method
        self.assertIs(neighbor.get_neighbors().pop(), self.node_a, "Neighbor not added")
        # Make sure the neighbor is not automatically updated
        self.assertEqual(self.node_a.get_neighbors(), set(),
                         "Neighbor list should not be updated automatically @Directed")
        # Make sure passing a Node instead of a list is handled correctly
        with self.assertRaises(AssertionError):
            Node(neighbor)

    def test_add_neighbors_at_init(self):
        """
        Test for passing multiple neighbors at initialising a Node.
        This includes a 500k node stress test.
        The test involves passing a large number of nodes and making sure the contents returned
        by the get_neighbors method is the same as what was passed at init.
        """
        # adding 5000 neighbors at init as a set
        neighbor_set = set()
        for _ in range(5000):
            neighbor_set.add(Node())
        many_node = Node(neighbor_set)
        self.assertEqual(many_node.get_neighbors(), neighbor_set, "Passing a large Neighbor list at Node Init fails")

        # stress test with set
        neighbor_set = set()
        for _ in range(500000):
            neighbor_set.add(Node())
        many_node = Node(neighbor_set)
        self.assertEqual(many_node.get_neighbors(), neighbor_set,
                         "Passing a VERY large Neighbor list at Node Init fails")

        # adding neighbors at init as a list
        neighbor_list = []
        for _ in range(50):
            neighbor_list.append(Node())
        many_node = Node(neighbor_list)
        self.assertEqual(many_node.get_neighbors(), set(neighbor_list),
                         "Passing a large Neighbor list at Node Init fails")

    def neighbor_already_added(self):
        """
        Tests situations where there is an attempt to add an existing neighbor.
        The expected handling of this is that there is no change to the neighbors as a Set is being used.
        """
        neighbor_a = Node()
        neighbor_b = Node()
        neighbor_c = Node()
        neighbor_d = Node()
        neighbor_e = Node()
        neighbors = {neighbor_a, neighbor_b, neighbor_c, neighbor_d, neighbor_e}
        self.node_a.add_neighbor(neighbors)
        previous_size = len(self.node_a.get_neighbors())
        for each in neighbors:
            self.node_a.add_neighbor(each)
        self.assertEqual(previous_size, self.node_a.get_neighbors, "Adding existing neighbors adds to the neighbor set")

    def test_add_neighbor(self):
        """
        Tests adding a neighbor using the add_neighbor method.
        The expected response is that an added node is returned via the get_neighbors() method.
        :return:
        """
        neighbor = Node()
        neighbor.add_neighbor(self.node_a)
        # Make sure the added node is accessible through the get method
        self.assertIs(neighbor.get_neighbors().pop(), self.node_a, "Neighbor not added")
        # Make sure the neighbor is not automatically updated as well
        self.assertEqual(self.node_a.get_neighbors(), set(),
                         'Neighbor list should not be updated automatically @Directed')

    def test_add_neighbors(self):
        """
        Test adding multiple neighbors to the node via add_neighbor()
        Includes multiple stress tests and attempts adding different types of sequences.
        :return:
        """
        neighbor_a = Node()
        neighbor_a.add_neighbor(*[self.node_a])
        self.assertIs(neighbor_a.get_neighbors().pop(), self.node_a, "Neighbor not added")
        self.assertEqual(self.node_a.get_neighbors(), set(),
                         "Neighbor list should not be updated automatically @Directed")

        # test passing a set
        assert len(self.node_a.get_neighbors()) == 0, "Test is incorrect"

        neighbor_set = set()
        for _ in range(500):
            neighbor_set.add(Node())
        self.node_a.add_neighbor(*neighbor_set)

        self.assertEqual(len(self.node_a.get_neighbors() - neighbor_set), 0)

        for _ in range(500000):
            neighbor_set.add(Node())
        self.node_a.add_neighbor(*neighbor_set)
        self.assertEqual(len(self.node_a.get_neighbors()), 500000 + 500)
        self.assertEqual(len(self.node_a.get_neighbors() - neighbor_set), 0)

        # test passing a list
        neighbor_list = []
        node_b = Node()
        for _ in range(500):
            neighbor_list.append(Node())
        node_b.add_neighbor(*neighbor_list)

        self.assertEqual(len(node_b.get_neighbors() - set(neighbor_list)), 0)

        for _ in range(500000):
            neighbor_list.append(Node())
        node_b.add_neighbor(*neighbor_list)
        self.assertEqual(len(node_b.get_neighbors()), 500000 + 500)
        self.assertEqual(len(node_b.get_neighbors() - set(neighbor_list)), 0)

        # test passing a tuple
        neighbor_list = []
        node_b = Node()
        for _ in range(500):
            neighbor_list.append(Node())
        neighbor_list = tuple(neighbor_list)
        node_b.add_neighbor(*neighbor_list)

        self.assertEqual(len(node_b.get_neighbors() - set(neighbor_list)), 0)

        # failure cases
        neighbor_set = set()
        for i in range(500):
            neighbor_set.add(i)
        neighbor_list = []
        for i in range(500):
            neighbor_list.append(i)
        with self.assertRaises(AssertionError):
            self.node_a.add_neighbor(*neighbor_set)
        with self.assertRaises(AssertionError):
            self.node_a.add_neighbor(*neighbor_list)

        node_c = Node([node_b])
        self.node_a.add_neighbor(*[node_b, node_c])
        neighbor_list = self.node_a.get_neighbors()
        self.assertIn(node_b, neighbor_list)
        self.assertIn(node_c, neighbor_list)

    def test_remove_node(self):
        """
        Tests the removal of nodes
        """
        neighbor_set = set()
        other_node = Node()
        for _ in range(5000):
            neighbor_set.add(Node())
        self.node_a.add_neighbor(*neighbor_set)
        self.node_a.add_neighbor(other_node)
        for each_node in neighbor_set:
            self.node_a.delete_neighbor(each_node)

        # Making sure the specified nodes are deleted
        self.assertEqual(self.node_a.get_neighbors(), {other_node})

        # Making sure there are no issues emptying the neighbor set
        self.node_a.delete_neighbor(other_node)

    def test_remove_exceptions(self):
        neighbor = Node()
        self.node_a.add_neighbor(neighbor)

        # testing removing a node that is not a neighbor
        self.assertRaises(AssertionError, self.node_a.delete_neighbor, Node())

        # testing again with non-empty neighbor list
        self.node_a.add_neighbor(neighbor)
        self.assertRaises(AssertionError, self.node_a.delete_neighbor, Node())
        # test passing a sequence
        self.assertRaises(AssertionError, self.node_a.delete_neighbor, [neighbor])
        self.assertRaises(AssertionError, self.node_a.delete_neighbor, {neighbor})
        # make sure nothing is broken
        self.node_a.delete_neighbor(neighbor)
        self.assertEqual(self.node_a.get_neighbors(), set())

    #todo test label
    #todo test attributes

if __name__ == "__main__":
    unittest.main()  # run all tests
