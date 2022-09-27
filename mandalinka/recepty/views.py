from xmlrpc.client import boolean
from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse, HttpResponseForbidden
from django.urls import reverse
from django.core.serializers import serialize
from django.utils.timezone import now
from django import forms

from recepty.models import Recipe, DeliveryDay


class NewRecipeForm(forms.Form):
    title = forms.CharField(label="Názov jedla", widget=forms.TextInput({'class':'form-control'}))
    prep_time = forms.IntegerField(label="Čas prípravy", min_value=1, max_value=90, required=False,  widget=forms.TextInput({'class':'form-control'}))

# Create your views here.
def index(request):
    return render(request, "recepty/landing_page.html", {
        "recipes": Recipe.objects.all(),
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

def load_next_order(request):
    if request.user.is_authenticated:
        delivery_day = DeliveryDay.objects.filter(date__gte=now().date()).order_by('date').first()
        recipes = []
        for recipeversion in delivery_day.recipes.all():

            # Add necessary info for desplay in recipe_widget here
            recipes.append({
                'title': recipeversion.recipe.title,
                'description': recipeversion.recipe.description,
            })

                
            if recipeversion.recipe.thumbnail:
                recipes[-1]["thumbnail"] = recipeversion.recipe.thumbnail.url
            else:
                recipes[-1]["thumbnail"] = None

        response = {
            'date': delivery_day.date,
            'recipes': recipes,
        }
        return JsonResponse(response)
        
    return HttpResponseForbidden(request)