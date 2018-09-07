import random

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from enron.models import Person
from enron.graph.graph import Graph

def index(request):
    return render(request, "enron/index.html", context={})


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

