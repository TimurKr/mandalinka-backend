import py_compile
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index')
]

