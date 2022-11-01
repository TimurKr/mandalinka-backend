from django.shortcuts import render
from django.http import HttpResponseBadRequest

# Create your views here.
def home_page_view(request):
    return HttpResponseBadRequest(request)