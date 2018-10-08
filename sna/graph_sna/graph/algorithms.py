"""
Collection of graph algorithms written for the Graph module.
"""
from graph_sna.graph.graph import Graph
from graph_sna.graph.node import Node
import math


class GraphAlgorithms:
    def __init__(self):
        # the following are variables used for the SCC algorithm
        self.time = 0
        self.current = []
        self.components = []
        pass

    @staticmethod
    def _health_check(graph):
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

    def average_edges_per_node(self, graph):
        return round(self.edge_count(graph) / self.node_count(graph), 2)

    def depth_first_search(self, graph, source):
        visited, stack = set(), [source]
        while stack:
            vertex = stack.pop()
            if vertex not in visited:
                visited.add(vertex)
                stack.extend(set(graph.get_node_neighbors(vertex)) - visited)
        return visited

    def discover_components(self, graph):
        all_nodes = set(graph.get_all_nodes())
        not_discovered = all_nodes.copy()
        components = []
        while not_discovered:
            currently_discovered = all_nodes - not_discovered
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
                if residual_capacity[(vertex, next)] > 0:  # if the edge has any flow capacity left
                    if next == goal:
                        return path + [next]  # end the first time a path is found
                    else:
                        queue.append((next, path + [next]))

    def collect_flow(self, path, residual_capacity_dict):
        """
        This method identifies how much flow is available through a given path and removes it from the
        residual capacity
        :return:
        """
        flow = math.inf
        for i, node in enumerate(path):
            if i != len(path) - 1:
                flow = min(flow, residual_capacity_dict[(path[i], path[i + 1])])

        for i, node in enumerate(path):
            if i != len(path) - 1:
                residual_capacity_dict[(path[i], path[i + 1])] -= flow

        return residual_capacity_dict, flow

    def edmonds_karp(self, graph, source, sink):
        # https://brilliant.org/wiki/edmonds-karp-algorithm/#algorithm-pseudo-code
        flow = 0  # start with flow = 0
        residual_capacity = {}  # this dictionary keeps track of how much capacity is left in an edge
        for edge in graph.get_all_edges():  # all the edges start at full capacity
            residual_capacity[(edge[0], edge[1])] = graph.get_weight(edge[0], edge[1])
        while True:
            P = self._bfs_flow_paths(graph, source, sink, residual_capacity)
            if P is None:  # if there is no path that can augment the flow, break
                break
            residual_capacity, m = self.collect_flow(P, residual_capacity)
            print(m)
            flow += m
        return flow, residual_capacity
        # i'm returning residual capcity back because it would be nice to highlight the paths here

    def local_clustering_coefficient(self, graph, node):
        outgoing_neighbors = graph.get_node_neighbors(node)
        incoming_neighbors = graph.get_incoming_neighbors(node)
        all_neighbors = incoming_neighbors.union(outgoing_neighbors)
        all_neighbors.add(node)
        # find the number of links between these.
        neighborhood_links = 0
        for neighborhood_nodes in all_neighbors:
            neighborhood_links += len(all_neighbors.intersection(graph.get_node_neighbors(neighborhood_nodes)))
        # number of possible neighbors
        max_neighbors = len(all_neighbors) * (len(all_neighbors) - 1)
        coefficient = neighborhood_links / max_neighbors
        return round(coefficient, 2)

    def average_clustering_coefficient(self, graph):
        total = 0
        for each_node in graph.get_all_nodes():
            total += self.local_clustering_coefficient(graph, each_node)
        return round(total / self.node_count(graph), 2)

    def min_cut_max_flow(self, graph, source, sink):
        """
        Finds the cut along the graph which contains the critical edges for the flow.
        As shown in the max-flow min-cut theorem, the weight of this cut equals the maximum amount of flow
        that can be sent from the source to the sink in the given network.
        :param graph:
        :param max_flow:
        :return:
        """
        min_cut = set()
        flow, residual_capacity = self.edmonds_karp(graph, source, sink)
        for key, value in residual_capacity.items():
            if value is 0:
                min_cut.add(key)
        return min_cut

    def strongly_connected_components(self, graph):
        """
        https://www.geeksforgeeks.org/tarjan-algorithm-find-strongly-connected-components/
        A strongly connected component is maximal subgraph of a directed graph such that for every pair of vertices  u, v
        in the subgraph, there is a directed path from u to v and a directed path from v to u.
        We use Tarjan's algorithm for this implementation
        :param graph:
        :return:
        """

        # Mark all the vertices as not visited
        # and Initialize parent and visited,
        # and ap(articulation point) arrays
        self.time = 0  # resetting this and it is incremented at each step of discovery
        node_count = self.node_count(graph)
        disc, low, stackMember = {}, {}, {}
        for i in graph.get_all_nodes():
            disc[i] = -1
            low[i] = -1
            stackMember[i] = False
        st = []

        # Call the recursive helper function
        # to find articulation points
        # in DFS tree rooted with vertex 'i'
        for i in graph.get_all_nodes():
            if disc[i] == -1:
                self.SCC_aux(i, low, disc, stackMember, st, graph)
        print(self.components)

    def SCC_aux(self, u, low, disc, stackMember, st, graph):
        """
        Helper function for strongly connected components.
        :return:
        """
        disc[u] = self.time
        low[u] = self.time
        self.time += 1
        stackMember[u] = True
        st.append(u)
        # Go through all vertices adjacent to this
        neighbors = graph.get_node_neighbors(u)
        for v in neighbors:  # iterating through all the outgoing edges of this node
            if disc[v] == -1:
                self.SCC_aux(v, low, disc, stackMember, st, graph)
                low[u] = min(low[u], low[v])
            elif stackMember[v]:
                low[u] = min(low[u], disc[v])

        w = -1  # To store stack extracted vertices
        if low[u] == disc[u]:
            while w != u:
                w = st.pop()
                self.add_to_current_component(w)
                stackMember[w] = False
            self.new_component()

    def add_to_current_component(self, node):
        self.current.append(node)

    def new_component(self):
        self.components.append(self.current)
        self.current = []
