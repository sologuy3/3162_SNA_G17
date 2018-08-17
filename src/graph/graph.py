from src.graph.node import Node

class Graph:
    def __init__(self, name, modifiable=False):
        self._graph = {}
        self._weights = {}
        self.statistics = {}
        self.name = name
        self.modifiable = modifiable

    def __str__(self):
        pass
        # TODO: Graph string with node count / edge count etc

    def has_node(self, node):

        """
        Returns wether the node is present in the graph
        :type node: Node
        """
        return node in self._graph


    def has_edge(self, node1, node2):

        """
        Returns True if an edge exists directed from node1 towards node2

        :type node1: Node
        :type node2: Node
        """

        assert self.has_node(node1), "node1 {} not present in graph".format(node1)
        assert self.has_node(node2), "node2 {} not present in graph".format(node2)
        assert node2 in self._graph[node1], "No connection exists between node1 {} and node2 {}".format(node1, node2)
        assert (node1, node2) in self._weights, "No weight for edge ({}, {})".format(node1, node2)
        return node1, node2 in self._weights


    def add_nodes(self, node, neighbors=None):

        """
        Add a node to the graph with specified neighbors

        :type neighbors: set
        :type node: Node
        """

        assert not self.has_node(node), "Node {} already exists in the graph".format(node)
        assert isinstance(neighbors, set), "Neighbors iterable is not a set"

        if neighbors is not None:
            self._graph[node] = neighbors

    def add_edge(self, node1, node2):

        """
        Add an edge directed from node1 towards node2
        :type node1: Node
        :type node2: Node
        :return:
        """

        assert not self.has_edge(node1, node2), "Edge from {} -> {} already exists".format(node1, node2)

        self._graph[node1].add(node2)
        node1.add_neighbor(node2)


    def update_node(self, old_node, new_node):

        """
        Replace a node with another node in its place

        :type old_node: Node
        :type new_node: Node
        """
        assert self.has_node(old_node), "Old node {} not in graph".format(old_node)
        assert not self.has_node(new_node), "New node {} not in graph".format(new_node)


        # Update node-level data
        for neighbor in self._graph[old_node]:
            neighbor.add_neighbor(new_node)
            neighbor.delete_neighbor(old_node)

        # New node has old nodes connections
        self._graph[new_node] = self._graph[old_node]

        # Remove old node key from the graph
        del self._graph[old_node]


    def update_edge(self, node1, node2, new_weight):

        """
        Update the value of a weight in the graph
        :type node1: Node
        :type node2: Node
        :type new_weight: float
        """
        assert self.has_edge(node1, node2), "No edge exists between node1 {} and node2 {}".format(node1, node2)
        self._weights[(node1, node2)] = new_weight

    def delete_edge(self, node1, node2):
        """
        Delete an edge spanning from node1 to node2
        :type node1: Node
        :type node2: Node
        """
        assert self.has_node(node1), "Node1 {} not in graph".format(node1)
        assert self.has_node(node2), "Node2 {} not in graph".format(node2)
        assert self.has_edge(node1, node2), "Edge from {} -> {} doesn't exist".format(node1, node2)

        node1.delete_neighbor(node2)
        self._graph[node1].remove(node2)
        del self._weights[(node1, node2)]


    def delete_node(self, node):
        """
        Obliterate a node out of existence.
        Deletes all edges spanning towards and away from it.

        :type node: Node
        """

        assert self.has_node(node)

        for neighbor in self._graph[node]:
            if self.has_edge(node, neighbor):
                self.delete_edge(node, neighbor)
            if self.has_edge(neighbor, node):
                self.delete_edge(neighbor, node)


    def get_node_neighbors(self, node):
        """
        Return a nodes neighbors
        :param node: Node
        :return: set
        """
        return self._graph[node]

    def get_node_edges(self, node):
        """
        Return list of edges from node
        :type node: Node
        :return: List
        """
        node_edges = []

        for neighbor in self._graph[node]:
            weight = 0 if not (node, neighbor) in self._weights else self._weights[(node,neighbor)]
            node_edges.append((node, neighbor, weight))

        return node_edges


    def get_all_nodes(self):
        """
        Return a list of all nodes in the graph
        :return: List
        """

        l = []

        for k, v in self._graph.items():

            # Each key represents a node in the graph
            l.append(k)

        return l

    def get_all_edges(self):
        """
        Return a list of all edges in the graph
        :return: List
        """
        l = []

        for k, v in self._weights.items():
            # k is the tuple, v is the weight
            l.append((k[0], k[1], v))

        return l

    def get_weight(self, node1, node2):
        """
        Return the weight of an edge
        :type node1: Node
        :type node2: Node
        :return: float
        """
        assert self.has_edge(node1, node2), "No edge exists between node1 {} and node2 {}".format(node1, node2)
        return self._weights[(node1, node2)]








