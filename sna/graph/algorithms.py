from sna.graph.graph import Graph
from sna.graph.node import Node
import math


class GraphAlgorithms:
    def __init__(self):
        pass

    def _health_check(self, graph):
        """
        Makes sure the graph is good
        :return:
        """
        if isinstance(graph, Graph):  # todo verify _graph vs _weights
            return True
        else:
            raise TypeError("Graph objected expected, got {} instead".format(str(type(graph))))

    def node_count(self, graph):
        return len(graph.get_all_nodes())

    def edge_count(self, graph):
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
            prev[v] = None  # previous node in optimal path from source
            q.add(v)

        dist[source] = 0

        while q:
            u = self._min_dist(q, dist)
            q.remove(u)

            for v in graph.get_node_neighbors(u):
                alt = dist[u] + graph.get_weight(u, v)
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

    def minimum_average_path(self, graph):
        sum = 0
        count = 0
        for each_node in graph.get_all_nodes():
            shortest_dist, prev = self.shortest_path_length(graph, each_node)
            for each in shortest_dist.values():
                if (each is not math.inf) and (each is not 0):  # ignores unreachable paths and self-paths
                    sum += each
                    count += 1
        return sum / count

    def diameter(self, graph):
        max = 0
        for each_node in graph.get_all_nodes():
            shortest_dist, prev = self.shortest_path_length(graph, each_node)
            for each in shortest_dist.values():
                if (each > max) and (each is not math.inf):
                    max = each
        return max

    def mode_path_length(self, graph):
        from collections import Counter
        all_shortest = []
        for each_node in graph.get_all_nodes():
            shortest_dist, prev = self.shortest_path_length(graph, each_node)
            all_shortest = all_shortest + [x for x in shortest_dist.values() if x not in (0, math.inf)]
        return Counter(all_shortest).most_common()[0]

    def median_path_length(self, graph):
        from statistics import median
        all_shortest = []
        for each_node in graph.get_all_nodes():
            shortest_dist, prev = self.shortest_path_length(graph, each_node)
            all_shortest = all_shortest + [x for x in shortest_dist.values() if x not in (0, math.inf)]
        return median(all_shortest)

    def average_edges_per_node(self,graph):
        return round(self.edge_count(graph)/self.node_count(graph), 2)

    def depth_first_search(self, graph, source):
        visited, stack = set(), [source]
        while stack:
            vertex = stack.pop()
            if vertex not in visited:
                visited.add(vertex)
                stack.extend(set(graph.get_node_neighbors(vertex)) - visited)
        return visited

    def discover_components(self,graph):
        all_nodes = set(graph.get_all_nodes())
        not_discovered = all_nodes.copy()
        components = []
        while not_discovered:
            currently_discovered = all_nodes-not_discovered
            current_source = not_discovered.pop()
            dfs_component = self.depth_first_search(graph, current_source)

            if dfs_component.intersection(currently_discovered):
                for i, each_discovered_component in enumerate(components):
                    if each_discovered_component.intersection(dfs_component):
                        components[i] = each_discovered_component.union(dfs_component)
            else:
                components.append(dfs_component)
                not_discovered -= dfs_component

        return components

    def _bfs_flow_paths(self, graph, start, goal, residual_capacity):
        queue = [(start, [start])]
        while queue:
            (vertex, path) = queue.pop(0)
            for next in set(graph.get_node_neighbors(vertex)) - set(path):
                if residual_capacity[(vertex,next)] > 0:       # if the edge has any flow capacity left
                    if next == goal:
                        return path + [next]        # end the first time a path is found
                    else:
                        queue.append((next, path + [next]))

    def collect_flow(self,path,residual_capacity_dict):
        """
        This method identifies how much flow is available through a given path and removes it from the
        residual capacity
        :return:
        """
        flow = math.inf
        for i,node in enumerate(path):
            if i != len(path)-1:
                flow = min(flow,residual_capacity_dict[(path[i],path[i+1])])

        for i,node in enumerate(path):
            if i != len(path)-1:
                residual_capacity_dict[(path[i],path[i+1])] -= flow


        return residual_capacity_dict, flow


    def edmonds_karp(self,graph,source,sink):
        # https://brilliant.org/wiki/edmonds-karp-algorithm/#algorithm-pseudo-code
        flow = 0        # start with flow = 0
        residual_capacity = {}      # this dictionary keeps track of how much capacity is left in an edge
        for edge in graph.get_all_edges():      # all the edges start at full capacity
            residual_capacity[(edge[0],edge[1])] = graph.get_weight(edge[0],edge[1])
        while True:
            P = self._bfs_flow_paths(graph,source,sink,residual_capacity)
            if P is None:   # if there is no path that can augment the flow, break
                break
            residual_capacity, m = self.collect_flow(P,residual_capacity)
            print(m)
            flow += m
        return flow,residual_capacity
        # i'm returning residual capcity back because it would be nice to highlight the paths here


    def local_clustering_coefficient(self,graph,node):
        outgoing_neighbors = graph.get_node_neighbors(node)
        incoming_neighbors = graph.get_incoming_neighbors(node)
        all_neighbors = incoming_neighbors.union(outgoing_neighbors)
        all_neighbors.add(node)
        # find the number of links between these.
        neighborhood_links = 0
        for neighborhood_nodes in all_neighbors:
            neighborhood_links += len(all_neighbors.intersection(graph.get_node_neighbors(neighborhood_nodes)))
        return neighborhood_links










