from xmlrpc.client import boolean
from django.shortcuts import render
from django.http import HttpResponse

class Krok():
    
    thumbnail = None
    postup_sk = None
    postup_en = None

    def __init__(self) -> None:
        pass


class Recept():
    thumbnail = "static"
    nazov = "Mandalinkový koláč"
    postup = [Krok() for i in range(6)]

    def __init__(self) -> None:
        pass


recepty = [Recept() for i in range(3)]

# Create your views here.
def index(request):
    return render(request, "recepty/recepty_homeview.html", {
        "recepty": recepty
    })

def novy_recept(request):
    return render(request, "recepty/novy_recept.html")