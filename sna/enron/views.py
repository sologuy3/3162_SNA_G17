from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from enron.models import Person

def index(request):
    return render(request, "enron/index.html", context={})


def get_enron(request):
    people = Person.objects.all()
    data = {}
    for person in people:
        data[person.email_address] = person.email_address
    return JsonResponse(data)
