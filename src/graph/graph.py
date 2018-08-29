from src.graph.node import Node

class Graph:
    def __init__(self, name, modifiable=False):
        self._graph = {}
        self._weights = {}
        self.statistics = {}
        self.name = name
        self.modifiable = modifiable

    def __str__(self):

        return self.name + ":\n\t"  + "\n\t".join([str(node) for node in self._graph.keys()]) + "\n----"
        # TODO: Graph string with node count / edge count etc

    def has_node(self, node):   # todo bugfix - there's something funky here

        """
        Returns wether the node is present in the graph
        :type node: Node
        """
        return node in self._graph

    def has_edge(self, node1, node2):   # todo bugfix - there's something funky here

        """
        Returns True if an edge exists directed from node1 towards node2

        :type node1: Node
        :type node2: Node
        """
        assert isinstance(node1,Node) and isinstance(node2,Node), "Both node1 and node2 must be Node objects"
        assert self.has_node(node1), "node1 {} not present in graph".format(node1)
        assert self.has_node(node2), "node2 {} not present in graph".format(node2)
        #assert node2 in self._graph[node1], "No connection exists between node1 {} and node2 {}".format(node1, node2)
        # YOHAN- I don't think raising an error here makes sense, should just return false
        if node2 in self._graph[node1]:
            if (node1, node2) not in self._weights:#"No weight for edge ({}, {}) ".format(node1, node2)
                raise ReferenceError("The edge {}:{} exists but has not been assigned a weight".format(node1, node2))
            else:
                return (node1, node2) in self._weights  # fixed lack of brackets - YF 25/8
        else:
            return False



    def add_node(self, node, neighbors=None):

        """
        Add a node to the graph with specified neighbors

        :type neighbors: set
        :type node: Node
        """
        assert node != neighbors, "please add self edges by adding the node individually first, instead of add_node()"
        assert not self.has_node(node), "Node {} already exists in the graph".format(node)
        assert isinstance(node,Node), "node needs to be a Node object"
        # changed this to check if not None first - Yohan 24/08
        if neighbors is not None:
            assert isinstance(neighbors, set), "Neighbors iterable is not a set"
            self._graph[node] = neighbors
            for neighbor in neighbors:
                self._weights[(node,neighbor)] = 0
                node.add_neighbor(neighbor)
        else:
            self._graph[node] = set()

            #for neighbor in neighbors:
            #    self.update_edge(node,neighbor,0)

    def add_edge(self, node1, node2):
        """
        Add an edge directed from node1 towards node2
        :type node1: Node
        :type node2: Node
        :return:
        """

        assert not self.has_edge(node1, node2), "Edge from {} -> {} already exists".format(node1, node2)

        self._graph[node1].add(node2)
        self._weights[(node1,node2)] = 0
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
        for other_node in self.get_all_nodes():
            # added copy to avoid RuntimeError: Set changed size during iteration - YF 26/08
            if self.has_edge(node, other_node):
                self.delete_edge(node, other_node)
            if self.has_edge(other_node, node):
                #print("B:",(neighbor, node))
                self.delete_edge(other_node, node)
                #print("A:",(neighbor, node))

        del self._graph[node]       # added this to remove node from graph fully YF 26/08


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

    def get_all_nodes(self,stringify=False):
        """
        Return a list of all nodes in the graph
        :return: List
        """

        l = []

        for k, v in self._graph.items():
            # Each key represents a node in the graph
            if stringify:
                l.append(str(k))
            else:
                l.append(k)

        return l

    def get_all_edges(self,stringify=False):
        """
        Return a list of all edges in the graph
        :return: List
        """
        l = []

        for k, v in self._weights.items():
            # k is the tuple, v is the weight
            if stringify:
                l.append("({}->{}: {})".format(str(k[0].label), str(k[1].label), v))
            else:
                l.append((k[0], k[1], v))

        return self.name + "weights: \n\t" + "\n\t".join(l) if stringify else l


    def get_weight(self, node1, node2):
        """
        Return the weight of an edge
        :type node1: Node
        :type node2: Node
        :return: float
        """
        assert self.has_edge(node1, node2), "No edge exists between node1 {} and node2 {}".format(node1, node2)
        return self._weights[(node1, node2)]
