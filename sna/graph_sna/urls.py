from django.urls import path

from . import views

urlpatterns = [
    path('get_enron.json', views.get_enron, name="get_enron"),
    path('get_test_graph.json', views.get_test_graph, name="get_test_graph"),
    path('', views.index, name='index'),
]