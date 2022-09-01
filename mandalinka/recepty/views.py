from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return render(request, "recepty/recepty_homeview.html")
def novy_recept(request):
    return HttpResponse("Na tejto stránke sa budú pridávať nové recepty")