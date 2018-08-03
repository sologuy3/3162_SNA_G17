class Node:

    def __init__(self, neighbors=None, label=None, attributes=None):

        """
        :param neighbors: [Node] array of this nodes neighbors
        :param label: Label for this ndoe
        :param attrs: __dict__ containing k->v attributes.
        """

        if neighbors is not None:
            assert isinstance(neighbors, list) , "Neighbors object is not a list"
            self.add_neighbors(*neighbors)

        self.label = label
        self.attributes = attributes

    def __getattribute__(self, item):
        assert item in self.attributes, "Key [{}] not found in attributes dict.".format(item)
        return self.attributes[item]


    def __str__(self):
        return "(Node, Neighbors, Data) = ({},[{}],{{{}}})".format(self.label, self.neighbors, self.attributes)


    def get_neighbors(self):
        """
        External method to get neighbors list
        For internal neighbor retrieval use self.neighbors
        :return: Neighbors list
        """
        return self.neighbors
        pass


    def add_neighbors(self, *neighbors):
        """
        Add a list of neighbors to the node
        :param neighbors: A starred list. Use add_neighbors(*list)
        :return: None
        """

        for potential_neighbor in neighbors:
            assert isinstance(potential_neighbor, Node), "{} is not a node".format(node)
            self.neighbors.append(potential_neighbor)

        # TODO: This should also update the Graph

    def delete_neighbor(self, neighbor):
        """
        Delete a neighbor from the list if it is present
        :param neighbor: The node to delete
        :return: None
        """
        assert isinstance(neighbor, Node), "Neighbor {} is not a node".format(neighbor)
        assert neighbor in self.neighbors, "{} not in neighbors list".format(neighbor)

        self.neighbors.remove(neighbor)


