import random

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from graph_sna.models import Person
from graph_sna.graph.graph import Graph

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

