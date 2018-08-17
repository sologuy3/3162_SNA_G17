import unittest
from src.graph.node import Node


class NodeTest(unittest.TestCase):
    def setUp(self):
        """Call before every test case."""
        self.node_a = Node()

    def tearDown(self):
        """Call after every test case."""

    def test_add_neighbor_at_init(self):
        """
        Test for passing a one neighbor as an argument when initializing a node.
        """
        neighbor = Node([self.node_a]) # initialise a new node to use for this test
        # Make sure the added node is accessible through the get method
        self.assertIs(neighbor.get_neighbors().pop(),self.node_a, "Neighbor not added")
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
        neighbor_set = set()
        for _ in range(5000):
            neighbor_set.add(Node())
        many_node = Node(neighbor_set)
        self.assertEqual(many_node.get_neighbors(), neighbor_set,"Passing a large Neighbor list at Node Init fails")

        neighbor_set = set()
        for _ in range(500000):
            neighbor_set.add(Node())
        many_node = Node(neighbor_set)
        self.assertEqual(many_node.get_neighbors(), neighbor_set,
                         "Passing a VERY large Neighbor list at Node Init fails")

        #todo add fail cases and other data structs

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
        neighbors={neighbor_a,neighbor_b,neighbor_c,neighbor_d,neighbor_e}
        self.node_a.add_neighbor(neighbors)
        previous_size = len(self.node_a.get_neighbors())
        for each in neighbors:
            self.node_a.add_neighbor(each)
        self.assertEqual(previous_size,self.node_a.get_neighbors,"Adding existing neighbors adds to the neighbor set")



    def test_add_neighbor(self):
        """
        Tests adding a neighbor using the add_neighbor method.
        The expected response is that an added node is returned via the get_neighbors() method.
        :return:
        """
        neighbor = Node()
        neighbor.add_neighbor(self.node_a)
        self.assertIs(neighbor.get_neighbors().pop(), self.node_a, "Neighbor not added")
        self.assertEqual(self.node_a.get_neighbors(), set(),
                          "Neighbor list should not be updated automatically @Directed")

        #todo add fail cases

    def test_add_neighbors(self):
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

        self.assertEqual(len(self.node_a.get_neighbors() - neighbor_set),0)


        for _ in range(500000):
            neighbor_set.add(Node())
        self.node_a.add_neighbor(*neighbor_set)
        self.assertEqual(len(self.node_a.get_neighbors()),500000+500)
        self.assertEqual(len(self.node_a.get_neighbors() - neighbor_set),0)

        # test passing a list
        neighbor_list = []
        node_b = Node()
        for _ in range(500):
            neighbor_list.append(Node())
        node_b.add_neighbor(*neighbor_list)

        self.assertEqual(len(node_b.get_neighbors() - set(neighbor_list)),0)

        for _ in range(500000):
            neighbor_list.append(Node())
        node_b.add_neighbor(*neighbor_list)
        self.assertEqual(len(node_b.get_neighbors()),500000+500)
        self.assertEqual(len(node_b.get_neighbors() - set(neighbor_list)),0)

        # test passing a tuple
        neighbor_list = []
        node_b = Node()
        for _ in range(500):
            neighbor_list.append(Node())
        neighbor_list = tuple(neighbor_list)
        node_b.add_neighbor(*neighbor_list)

        self.assertEqual(len(node_b.get_neighbors() - set(neighbor_list)),0)

        #failure cases
        neighbor_set = set()
        for i in range(500):
            neighbor_set.add(i)
        neighbor_list = []
        for i in range(500):
            neighbor_list.append(i)
        with self.assertRaises(AssertionError):
            self.node_a.add_neighbor(*neighbor_set)
            self.node_a.add_neighbor(*neighbor_list)

        node_c = Node([node_b])
        self.node_a.add_neighbor(*[node_b,node_c])
        neighbor_list = self.node_a.get_neighbors()
        self.assertIn(node_b,neighbor_list)
        self.assertIn(node_c,neighbor_list)

    #todo deleteNode

if __name__ == "__main__":
    unittest.main()     # run all tests
