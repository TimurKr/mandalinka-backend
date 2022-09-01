from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return HttpResponse("Táto stránka bude zobrazovať zoznam pridaných receptov")

def novy_recept(request):
    return HttpResponse("Na tejto stránke sa budú pridávať nové recepty")