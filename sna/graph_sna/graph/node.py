class Node:

    def __init__(self, neighbors=None, label=None, attributes=None):

        """
        :param neighbors: [Node] set of this nodes neighbors
        :param label: Label for this ndoe
        :param attrs: __dict__ containing k->v attributes.
        """

        # Internally stored as a python set for O(1) containment checking
        # Do not access / modify directly
        self._neighbors = set()

        if neighbors is not None:
            assert isinstance(neighbors, set) or isinstance(neighbors, list), "Neighbors object is not a set or list"
            self.add_neighbor(*neighbors)

        self.label = label
        self.attributes = attributes

    def __getitem__(self, item):
        assert item in self.attributes, "Key [{}] not found in attributes dict of node \n\t {}.".format(item, self)
        return self.attributes[item]

    def __setitem__(self, key, value):
        self.attributes[key] = value

    def __repr__(self):
        return str(self.label)

    def __str__(self):
        return "Name: {} | Neighbors: [{}] | Attributes: {{{}}})".format(self.label, self.get_neighbors(stringify=True),
                                                                         str(self.attributes))

    def get_neighbors(self, stringify=False):
        """
        External method to get neighbors list
        For internal neighbor retrieval use self._neighbors
        :return: Neighbors list
        """
        if stringify:
            neighbor_string = ''
            if self._neighbors or len(self._neighbors):
                for neighbor in self._neighbors:
                    neighbor_string = neighbor_string + str(neighbor.label)
                return neighbor_string

            else:
                return 'No Neighbors'

        else:
            return self._neighbors

    def add_neighbor(self, *neighbors):
        """
        Add an arbitrary argument list of neighbors to the node
        :param neighbors: A starred list. Use add_neighbor(*List[Node]) or add_neighbor(Node)
        :return: None
        """

        for potential_neighbor in neighbors:
            assert isinstance(potential_neighbor, Node), "{} is not a node".format(potential_neighbor)
            self._neighbors.add(potential_neighbor)

        # This should also update the Graph
        # Graph will manage this - YF

    def delete_neighbor(self, neighbor):
        """
        Delete a neighbor from the list if it is present
        :param neighbor: The node to delete
        :return: None
        """
        assert isinstance(neighbor, Node), "Neighbor {} is not a node".format(str(neighbor))
        assert neighbor in self._neighbors, "{} not in neighbors set".format(str(neighbor))

        self._neighbors.remove(neighbor)

    def save_repr(self):
        return str(self.label)
