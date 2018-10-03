import csv,json
from sna.graph_sna.graph.graph import Graph
from sna.graph_sna.graph.graph import Node


def handle_create_edge(graph, node, neighbor):
    """
    The job of this function is to check if the edge exists, and if not create it.
    If the edge exists, just increment its weight.
    This function adds the edge both ways.
    :param graph:
    :param node:
    :param neighbor:
    :return:
    """
    # one way
    if graph.has_edge(node, neighbor):
        graph.update_edge(node, neighbor, graph.get_weight(node, neighbor) + 1)
    else:
        graph.add_edge(node, neighbor, 1)
    # the other way
    if graph.has_edge(neighbor, node):
        graph.update_edge(neighbor, node, graph.get_weight(neighbor, node) + 1)
    else:
        graph.add_edge(neighbor, node, 1)

    return graph


class reposts:
    def __init__(self):

        self.reposters = dict()
        self.subredditors = dict()
        self.graph = None

    def parse(self):
        filename = 'submissions.csv'
        csv_file = open(filename, 'r', encoding="utf-8")
        csv_reader = csv.reader(csv_file)
        #csv_reader.__next__()  # skip header
        count = 0
        for line in csv_reader:
            try:
                image_id = line[0]
                subreddit = line[7]
                uname = line[12]

                if image_id is '' or subreddit is '' or uname is '':
                    print("missing field at line {}".format(csv_reader.line_num))
                    count += 1
                else:

                    if subreddit in self.subredditors.keys():
                        self.subredditors[subreddit].add(uname)
                    else:
                        self.subredditors[subreddit] = {uname}

                    if image_id in self.reposters.keys():
                        self.reposters[image_id].add(uname)
                    else:
                        self.reposters[image_id] = {uname}

            except IndexError:
                print("Not enough elements at line {}".format(csv_reader.line_num))
        print("percentage of unuseable data is {}".format((count/csv_reader.line_num)*100))

    def generate_graph(self):
        out_graph = Graph(name="Reddit Graph")
        user_node_map = {}  # make it a bit faster than doing a label lookup
        # initialise all the nodes
        all_users = set()
        for img, users in self.reposters.items():
            for each in users:
                all_users.add(each)

        for user in all_users:
            print(user)
            node = Node(label=user)
            out_graph.add_node(node)
            user_node_map[user] = node

        for image, users in self.reposters.items():
            for user in users:
                for neighbor in users:
                    if user is not neighbor:
                        if user is not '' and neighbor is not '':
                            out_graph = handle_create_edge(out_graph, user_node_map[user], user_node_map[neighbor])
        return out_graph


if __name__ == "__main__":
    reddit = reposts()
    reddit.parse()

    graph = reddit.generate_graph()

    with open('redditdump','w+') as redditdump:
        redditdump.write(json.dumps(graph.dump_graph(weight_threshold=graph.get_threshold(25))))


