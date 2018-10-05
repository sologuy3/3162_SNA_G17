import random, json

from django.http import JsonResponse
from django.shortcuts import render
from graph_sna.models import Person
from graph_sna.graph.sample_graphs import graph_c
from graph_sna.graph.graph import Graph
from graph_sna.graph.testAlgorithms import initialise_sample_graph

def index(request):
    return render(request, "graph_sna/index.html", context={})


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

def get_test_graph(request):
    gc = initialise_sample_graph(graph_c)
    assert isinstance(gc, Graph)
    dump = gc.dump_graph()
    reddit = json.loads(open("redditdump").read())
    return JsonResponse(reddit)