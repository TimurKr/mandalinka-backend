import py_compile
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('novy_recept', views.novy_recept, name='novy_recept')
]

