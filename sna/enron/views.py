import random

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from enron.models import Person

def index(request):
    return render(request, "enron/index.html", context={})


def get_enron(request):
    people = Person.objects.all()
    data = {'nodes': [], 'links': []}
    for person in people[:100]:
        data['nodes'].append({'id': person.email_address, 'group': 1})

    for i in range(1000):
        data['links'].append({'source': random.choice(data['nodes'])['id'],
                              'target': random.choice(data['nodes'])['id'],
                              'value': 1})

    return JsonResponse(data)
