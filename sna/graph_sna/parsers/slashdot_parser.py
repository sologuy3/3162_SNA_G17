from sna.graph_sna.graph.graph import Graph
from sna.graph_sna.graph.node import Node
from sna.graph_sna.graph.algorithms import GraphAlgorithms


class FriendOrFoe:
    def __init__(self):
        self.friend_foe = []
        self.users = set()
        self.graph = None

    def parse(self):
        filename = 'Slashdot0902.txt'
        slashfile = open(filename)
        for slashline in slashfile.readlines():
            if slashline[0] is not '#':
                slashline = slashline.strip('\n').split('\t')
                assert len(slashline) == 2
                self.users.add(slashline[0])
                self.users.add(slashline[1])
                self.friend_foe.append(tuple(slashline))

    def generate_graph(self):
        """
        To be used after the data is loaded using parse()
        :return:
        """
        self.graph = Graph('Slashdot')
        labelmap = {key:Node(label=key) for key in self.users}
        for k,v in labelmap.items():
            self.graph.add_node(v)
        for edge in self.friend_foe:
            self.graph.add_edge(labelmap[edge[0]],labelmap[edge[1]])
        return self.graph

if __name__ == "__main__":
    slashdata = FriendOrFoe()
    slashdata.parse()
    slashdot_graph = slashdata.generate_graph()

    with open('slashsave','w+') as slashsave:
        slashsave.write(slashdot_graph.get_save())