from xmlrpc.client import boolean
from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse, HttpResponseBadRequest
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
    delivery_day = DeliveryDay.objects.filter(date__gte=now().date()).order_by('date').first()
    recipes = {}
    attrs = {}
    
    if request.user.is_authenticated:
        user_food_pref = [a.attr for a in request.user.profile.food_preferences.all()]
    else:
        user_food_pref = []
    
    try: # Needs review
        order = request.user.orders.get(delivery_day_id = delivery_day.id)
    except:
        return HttpResponseBadRequest()

    for recipeversion in delivery_day.recipes.all():
        # Add necessary info for display in recipe_widget here

        if recipeversion.recipe.pescetarian:
            type = "pescetarian"
        elif recipeversion.recipe.vegetarian:
            type = "vegetarian"
        elif recipeversion.recipe.vegan:
            type = "vegan"
        else:
            type = "meat"

        try: 
            order_instance = order.recipe_instance.get(recipe_id = recipeversion.id)
            num_por = order_instance.portions
        except:
            return HttpResponseBadRequest()

        recipes[order_instance.id] = {
            'title': recipeversion.recipe.title,
            'description': recipeversion.recipe.description,
            'type': type,
            # 'attributes': [i.attr for i in recipeversion.recipe.attributes.all()],
            'alergens': recipeversion.get_alergens(),
            'amount': num_por,
            'price': recipeversion.get_price(),
        }

            
        if recipeversion.recipe.thumbnail:
            recipes[order_instance.id]["thumbnail"] = recipeversion.recipe.thumbnail.url
        else:
            recipes[order_instance.id]["thumbnail"] = None

        for attr in [i.attr for i in recipeversion.recipe.attributes.all()]:
            if attr not in attrs.keys():
                attrs[attr] = {
                    'recipes': [],
                    'favorite': False,
                    'selected': False,
                }
                if request.user.is_authenticated and attr in user_food_pref:
                    attrs[attr]['favorite'] = True
            attrs[attr]['recipes'].append(str(order_instance.id))


        
            

    response = {
        'date': delivery_day.date,
        'pickup': order.pickup,
        'order_id': order.id,
        'recipes': recipes,
        'attributes': attrs
    }
    return JsonResponse(response)

    