from graph_sna.graph.node import Node
import json

class Graph:
    def __init__(self, name, modifiable=False):
        self._graph = {}
        self._weights = {}
        self._labels = {}
        self.statistics = {}
        self.name = name
        self.modifiable = modifiable

    def __str__(self):

        return self.name + ":\n\t"  + "\n\t".join([str(node) for node in self._graph.keys()]) + "\n----"
        # TODO: Graph string with node count / edge count etc

    def has_node(self, node: Node):

        """
        Returns wether the Node object is present in the graph
        :type node: Node
        """
        return node in self._graph


    def has_node_by_label(self, node_label: str):

        """
        Returns wether the Node object is present in the graph
        :type node_label: Label of the node
        """
        return node_label in self._labels

    def has_edge(self, node1, node2):

        """
        Returns True if an edge exists directed from node1 towards node2

        :type node1: Node
        :type node2: Node
        """
        #assert isinstance(node1,Node) and isinstance(node2,Node), "Both node1 and node2 must be Node objects"
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
        #assert isinstance(node,Node), "node needs to be a Node object"
        # changed this to check if not None first - Yohan 24/08
        if neighbors is not None:
            assert isinstance(neighbors, set), "Neighbors iterable is not a set"
            self._graph[node] = neighbors
            for neighbor in neighbors:
                self._weights[(node,neighbor)] = 1
                node.add_neighbor(neighbor)
        else:
            self._graph[node] = set()

        self._labels[node.label] = node

            #for neighbor in neighbors:
            #    self.update_edge(node,neighbor,0)

    def add_edge(self, node1, node2, weight=1):
        """
        Add an edge directed from node1 towards node2
        :type node1: Node
        :type node2: Node
        :return:
        """

        assert not self.has_edge(node1, node2), "Edge from {} -> {} already exists".format(node1, node2)

        self._graph[node1].add(node2)
        self._weights[(node1,node2)] = weight
        node1.add_neighbor(node2)


    def update_node(self, old_node, new_node):

        """
        Replace a node with another node in its place

        :type old_node: Node
        :type new_node: Node
        """
        assert self.has_node(old_node), "Old node {} not in graph".format(old_node)
        assert not self.has_node(new_node), "New node {} in graph".format(new_node)


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

    def get_incoming_neighbors(self, node):
        """
        Get the nodes for incoming edges for a given node
        :param node:
        :return:
        """
        incoming_neighbors = set()
        for i_node in self._graph:
            if node in self._graph[i_node]:
                incoming_neighbors.add(i_node)

        return incoming_neighbors


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
        :return: List[Node]
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
        :return: List[Node, Node, Float]
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

    def get_node_from_label(self,label):
        """
        O(1) method to find a node by its
        :param label:
        :return:
        """
        if self.has_node_by_label(label):
            return self._labels[label]


    def dump_graph(self, weight_threshold=0, degree_threshold=0):
        """
        Convert a graph from internal representation to d3.js ready representation
        The representation is a dictionary of the following format:

                            data = {'nodes':[{'id': 'one', 'group': 1},
                        {'id': 'two', 'group': 1},
                        {'id': 'three', 'group': 1}
                        <!--- more nodes allowed --->],
                'links':[{'source': 'one', 'target': 'two', 'value': 1},
                        {'source': 'two', 'target': 'three', 'value': 1}
                        <!--- more edges allowed --->}]
                }

        :type graph: Graph
        """

        data = {'nodes': [], 'links': []}
        added_nodes = set()

        # node degree thresholding
        filtered_nodes = set()
        for node in self.get_all_nodes():
            if len(node.get_neighbors())>degree_threshold:
                filtered_nodes.add(node)

        # edge weight thresholding
        for edge in self.get_all_edges():
            if edge[2] > weight_threshold and edge[0] in filtered_nodes and edge[1] in filtered_nodes:
                data['links'].append({'source': edge[0].label, 'target': edge[1].label, 'value': edge[2]-weight_threshold})
                added_nodes.add(edge[1])
                added_nodes.add(edge[0])

        for node in self.get_all_nodes():
            if node in added_nodes and node in filtered_nodes:
                data['nodes'].append({'id': node.label, 'group': 1})
        return data

    def get_threshold(self,threshold):
        """
        threshold - the percentage where to set the threshold.
        Retursn a WEIGHT such that the weights above the given weight add up to the given threshold.
        For example, setting threshold = 25% gives you a weight such that 25% of the edges of the graph are
        higher than that weight.
        :return:
        """
        weightlist = sorted(list(self._weights.values()))
        index_cutoff = len(weightlist)*((100-threshold)/100)
        return weightlist[int(index_cutoff)]

    def get_save(self):
        out_dict = {}
        for node,neighbors in self._graph.items():
            out_dict[node.save_repr()] = [x.save_repr() for x in neighbors]
        out_links = {}
        for edge_pair,weighting in self._weights.items():
            key = edge_pair[0].save_repr()+'+:+'+edge_pair[1].save_repr()
            out_links[key] = weighting

        output = json.dumps(dict(nodes=out_dict,weights=out_links))
        return output

    def load_save(self,save, weight_threshold=0, degree_threshold=0):
        import json
        # reset
        self._graph = {}
        self._weights = {}

        save_dict = json.loads(save)
        nodes = save_dict['nodes']

        label_map = {}

        for node_label,neighbors in nodes.items():
            if len(neighbors) >= degree_threshold:
                crnt = Node(label=node_label)
                label_map[node_label] = crnt
                self.add_node(crnt)

        weights = save_dict['weights']
        
        for pair, weight in weights.items():
            (node,neighbor) = pair.split('+:+')
            if weight >= weight_threshold:
                try:
                    self.add_edge(label_map[node],label_map[neighbor],weight)
                except:
                    pass    # todo handle exceptions here properly + check whether the nodes are alredy in the graph.
