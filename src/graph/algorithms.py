from src.graph.graph import Graph
from src.graph.node import Node
import math
import heapq


class GraphAlgorithms:
    def __init__(self):
        pass

    def _health_check(self, graph):
        """
        Makes sure the graph is good
        :return:
        """
        if isinstance(graph, Graph):
            return True
        else:
            raise TypeError("Graph objected expected, got {} instead".format(str(type(graph))))

    def node_count(self, graph):
        self._health_check(graph)
        return len(graph.get_all_nodes())

    def edge_count(self,  graph):
        self._health_check(graph)
        return len(graph.get_all_edges())

    def shortest_path_length(self, graph, source):
        # plan is to do it in O(mn) then optimise to O(m logn) using pqueue
        assert isinstance(source, Node)
        q = set()
        dist = {}
        prev = {}
        all_nodes = set(graph.get_all_nodes())

        for v in all_nodes:  # initialization
            dist[v] = math.inf  # unknown distance from source to v
            prev[v] = None   # previous node in optimal path from source
            q.add(v)

        dist[source] = 0

        while q:
            u = self._min_dist(q, dist)
            q.remove(u)

            for v in graph.get_node_neighbors(u):
                alt = dist[u] + graph.get_weight(u,v)
                if alt < dist[v]:
                    dist[v] = alt
                    prev[v] = u

        return dist, prev

    def _min_dist(self, q, dist):
        """
        Returns the node with the smallest distance in q.
        Implemented to keep the main algorithm clean.
        """
        min_node = None
        for node in q:
            if min_node is None:
                min_node = node
            elif dist[node] < dist[min_node]:
                min_node = node

        return min_node


