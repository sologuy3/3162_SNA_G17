import random, json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from graph_sna.models import Person
from graph_sna.graph.sample_graphs import graph_c
from graph_sna.graph.graph import Graph
from graph_sna.graph.algorithms import GraphAlgorithms

from graph_sna.graph.testAlgorithms import initialise_sample_graph

current = None  # global variable to keep track of what graph is currently being shown.
# the default graph is laoded at the bottom of this (run at import)


def index(request):
    return render(request, "graph_sna/index.html", context={})


def reddit(request):
    return render(request, "graph_sna/reddit.html", context={})


def load_enron(request):
    with open('enronsave') as enron_save:
        enron_graph = Graph('enron')
        enron_graph.load_save(enron_save.read())
        global current
        current = enron_graph

    dump = enron_graph.dump_graph(weight_threshold=0, degree_threshold=0)
    with open('dump', 'w+') as dumpfile:
        dumpfile.write(json.dumps(dump))

    return render(request, "graph_sna/index.html", context={})


def load_reddit(request):
    global current
    with open('redditsave') as reddit_save:
        reddit_graph = Graph('reddit')
        reddit_graph.load_save(reddit_save.read(),weight_threshold=2,degree_threshold=3)
        global current
        current = reddit_graph
    print(reddit_graph.get_threshold(10))
    dump = reddit_graph.dump_graph(weight_threshold=2, degree_threshold=15)
    with open('dump', 'w+') as dumpfile:
        dumpfile.write(json.dumps(dump))

    return render(request, "graph_sna/index.html", context={})


def load_slashdot(request):
    with open('slashsave') as slash_save:
        slashdot_graph = Graph('slashdot')
        slashdot_graph.load_save(slash_save.read())
        global current
        current = slashdot_graph
    dump = slashdot_graph.dump_graph(degree_threshold=250)
    with open('dump', 'w+') as dumpfile:
        dumpfile.write(json.dumps(dump))

    return render(request, "graph_sna/index.html", context={})


def load_graph(request):
    current_graph_dump = json.loads(open("dump").read())
    return JsonResponse(current_graph_dump)


@csrf_exempt  # this decorator bypasses the need for CSRF Tokens
def run_algorithm(request):
    global current
    response_string = "Unknown Input"

    print(request)

    if request.method == 'GET':
        alg = request.GET['type']
        print(alg)
        valid_algorithms = ['node_count', 'edge_count', 'diameter', 'minimum_average_path', 'mode_path_length',
                            'average_edges_per_node', 'discover_components', 'acc', 'scc','holes']

        if alg in valid_algorithms:
            algrunner = GraphAlgorithms()  # initiliase graph algorithms class
            assert(isinstance(current,Graph)), "No active graph found"
            graph = current
            print("Graph Loaded")

            if alg == 'node_count':
                print('running '+alg)
                response_string = "Node Count:{}".format(str(algrunner.node_count(graph)))

            if alg == 'edge_count':
                print('running '+alg)
                response_string = "Edge Count:{}".format(str(algrunner.edge_count(graph)))

            if alg == 'diameter':
                print('running '+alg)
                response_string = "Diameter:{}".format(str(algrunner.diameter(graph)))

            if alg == 'minimum_average_path':
                print('running '+alg)
                response_string = "Average Minimum Path:{}".format(str(algrunner.minimum_average_path(graph)))

            if alg == 'mode_path_length':
                print('running '+alg)
                response_string = "Mode Path Length:{}".format(str(algrunner.mode_path_length(graph)))

            if alg == 'average_edges_per_node':
                print('running '+alg)
                response_string = "Average Edges per Node:{}".format(str(algrunner.average_edges_per_node(graph)))

            if alg == 'discover_components':
                print('running '+alg)
                response_string = str(algrunner.discover_components(graph))

            if alg == 'acc':
                print('running '+alg)
                response_string = "Average Clustering Coefficient:{}".format(str(algrunner.average_clustering_coefficient(graph)))

            if alg == 'scc':
                print('running '+alg)
                response_string = "Strongly Connected components:{}".format(str(algrunner.strongly_connected_components(graph)))

            if alg == 'holes':
                print('running '+alg)
                response_string = "Structural Holes:{}".format(str(algrunner.structural_holes(graph)))

    if request.method == "POST":
        valid_algorithms = ['spl','dfs','ek','lcc','mcmf']
        try:
            algtype = request.GET['type']
            in1 = request.GET['in1']
            in2 = request.GET['in2']
            print('alg: ' + algtype)
            print('in1: ' + in1)
            print('in2: ' + in2)

            algrunner = GraphAlgorithms()  # initiliase graph algorithms class
            assert(isinstance(current,Graph)), "No active graph found"
            graph = current
            print("Graph Loaded")

            if algtype == 'None':
                response_string = "You need to select an algorithm before submitting!"
            elif algtype in valid_algorithms:
                if algtype == 'spl':
                    try:
                        in1_node = graph.get_node_from_label(in1)
                        response_string = str(algrunner.shortest_path_length(graph,in1_node))
                    except Exception as err:
                        response_string = str(err)

                if algtype == 'dfs':
                    try:
                        in1_node = graph.get_node_from_label(in1)
                        response_string = str(algrunner.shortest_path_length(graph,in1_node))
                    except Exception as err:
                        response_string = str(err)

                if algtype == 'ek':
                    try:
                        in1_node = graph.get_node_from_label(in1)
                        in2_node = graph.get_node_from_label(in2)
                        response_string = str(algrunner.edmonds_karp(graph,in1_node,in2_node))
                    except Exception as err:
                        response_string = str(err)

                if algtype == 'lcc':
                    try:
                        in1_node = graph.get_node_from_label(in1)
                        response_string = str(algrunner.local_clustering_coefficient(graph,in1_node))
                    except Exception as err:
                        response_string = str(err)

                if algtype == 'mcmf':
                    try:
                        in1_node = graph.get_node_from_label(in1)
                        in2_node = graph.get_node_from_label(in2)
                        response_string = str(algrunner.min_cut_max_flow(graph,in1_node,in2_node))
                    except Exception as err:
                        response_string = str(err)
            else:
                response_string = "App error: No input"

        except KeyError:
            response_string = ("You need to select an algorithm before submitting!")
    print(response_string)
    response = HttpResponse(response_string)
    response['Access-Control-Allow-Origin'] = '*'  # in case we switch out the URL
    return response




load_enron(None)  # default graph is this.
