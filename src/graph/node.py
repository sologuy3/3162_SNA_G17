class Node:

    def __init__(self, neighbors=None, label=None, attributes=None):

        """
        :param neighbors: [Node] array of this nodes neighbors
        :param label: Label for this ndoe
        :param attrs: __dict__ containing k->v attributes.
        """
        self.neighbors = set()


        if neighbors is not None:
            assert isinstance(neighbors, set) or isinstance(neighbors,list) , "Neighbors object is not a set or list"
            self.add_neighbor(*neighbors)

        self.label = label
        self.attributes = attributes

    def __getitem__(self, item):
        assert item in self.attributes, "Key [{}] not found in attributes dict of node \n\t {}.".format(item, self)
        return self.attributes[item]

    def __setitem__(self, key, value):
        self.attributes[key] = value


    def __str__(self):
        return "Name: {} | Neighbors: [{}] | Attributes: {{{}}})".format(self.label, self.neighbors, self.attributes)


    def get_neighbors(self):
        """
        External method to get neighbors list
        For internal neighbor retrieval use self.neighbors
        :return: Neighbors list
        """
        return self.neighbors


    def add_neighbor(self, *neighbors):
        """
        Add an arbitrary argument list of neighbors to the node
        :param neighbors: A starred list. Use add_neighbor(*List[Node]) or add_neighbor(Node)
        :return: None
        """

        for potential_neighbor in neighbors:
            assert isinstance(potential_neighbor, Node), "{} is not a node".format(potential_neighbor)
            self.neighbors.add(potential_neighbor)

        # TODO: This should also update the Graph


    def delete_neighbor(self, neighbor):
        """
        Delete a neighbor from the list if it is present
        :param neighbor: The node to delete
        :return: None
        """
        assert isinstance(neighbor, Node), "Neighbor {} is not a node".format(neighbor)
        assert neighbor in self.neighbors, "{} not in neighbors set".format(neighbor)

        self.neighbors.remove(neighbor)

