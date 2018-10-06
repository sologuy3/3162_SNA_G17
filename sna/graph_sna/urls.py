from django.urls import path

from . import views

urlpatterns = [
    path('reddit', views.load_reddit, name="load_reddit"),
    path('slashdot', views.load_slashdot, name="load_slashdot"),
    path('load_graph.json', views.load_graph, name="load_graph"),
    path('reload',views.index, name='index'),
    path('', views.index, name='index'),
]