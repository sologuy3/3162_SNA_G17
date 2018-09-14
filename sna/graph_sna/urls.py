from django.urls import path

from . import views

urlpatterns = [
    path('get_enron.json', views.get_enron, name="get_enron"),
    path('', views.index, name='index'),

]
