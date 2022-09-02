from xmlrpc.client import boolean
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms

from recepty.models import Recipe

class Step():
    
    thumbnail = None
    instructions_sk = None
    instructions_en = None

    def __init__(self) -> None:
        pass


# class Recipe():
#     thumbnail = None
#     title = None
#     prep_time = None
#     steps = [Step() for i in range(6)]

#     def __init__(self) -> None:
#         pass

class NewRecipeForm(forms.Form):
    title = forms.CharField(label="Názov jedla", widget=forms.TextInput({'class':'form-control'}))
    prep_time = forms.IntegerField(label="Čas prípravy", 
    min_value=1, max_value=90, required=False,  widget=forms.TextInput({'class':'form-control'}))

# Create your views here.
def index(request):
    return render(request, "recepty/recepty_homeview.html", {
        "recipes": Recipe.objects.all(),
        "head":"Pozrite si naše recepty"
    })

def novy_recept(request):
    if request.method == "POST":

        form = NewRecipeForm(request.POST)
        if form.is_valid():
            r = Recipe(title=form.cleaned_data["title"], prep_time=form.cleaned_data["prep_time"])
            r.save()
            return HttpResponseRedirect(reverse("recepty:index"))

        else:
            return render(request, "recepty/novy_recept.html", {
                "form": form,
                "head":"Pridajte recept"
            })

    return render(request, "recepty/novy_recept.html",{
        "form": NewRecipeForm(),
        "head":"Pridajte recept"
    })