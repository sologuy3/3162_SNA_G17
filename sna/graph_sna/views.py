import random, json

from django.http import JsonResponse
from django.shortcuts import render
from graph_sna.models import Person
from graph_sna.graph.sample_graphs import graph_c
from graph_sna.graph.graph import Graph
from graph_sna.graph.testAlgorithms import initialise_sample_graph

def index(request):
    return render(request, "graph_sna/index.html", context={})

def reddit(request):
    return render(request, "graph_sna/reddit.html", context={})


def get_enron(request):
    people = Person.objects.all()[:100]
    data = {'nodes': [], 'links': []}

    for person in people:
        data['nodes'].append({'id': person.email_address, 'group': 1})


    for i in range(200):
        data['links'].append({'source': random.choice(data['nodes'])['id'],
                              'target': random.choice(data['nodes'])['id'],
                              'value': 1})

    return JsonResponse(data)

def load_reddit(request):
    with open('redditsave') as reddit_save:
        reddit_graph = Graph('reddit')
        reddit_graph.load_save(reddit_save.read())
    dump = reddit_graph.dump_graph(weight_threshold=reddit_graph.get_threshold(10),degree_threshold=15)
    with open('dump','w+') as dumpfile:
        dumpfile.write(json.dumps(dump))

    return render(request, "graph_sna/index.html", context={})

def load_slashdot(request):
    with open('slashsave') as slash_save:
        slashdot_graph = Graph('slashdot')
        slashdot_graph.load_save(slash_save.read())
    dump = slashdot_graph.dump_graph(degree_threshold=250)
    with open('dump','w+') as dumpfile:
        dumpfile.write(json.dumps(dump))

    return render(request, "graph_sna/index.html", context={})


def load_graph(request):
    gc = initialise_sample_graph(graph_c)
    assert isinstance(gc, Graph)
    dump = gc.dump_graph()
    reddit = json.loads(open("dump").read())
    return JsonResponse(reddit)




