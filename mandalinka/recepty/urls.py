import py_compile
from django.urls import path

from . import views

app_name = "recepty"

urlpatterns = [
    path('', views.index, name='index'),
    path('novy_recept', views.novy_recept, name='novy_recept'),
    path('load_recepty', views.load_recepty, name='load_recepty'),
]

