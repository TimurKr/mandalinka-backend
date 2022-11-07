from django.shortcuts import render

from django.contrib.auth.decorators import login_required, permission_required
from django.http import *
from django.urls import reverse

from .models import Recipe
from . import forms


# RECIPES ######################################################################################

# LIST
@permission_required('recipes.view_recipe')
def list_recipes(request):
    recipes = Recipe.objects.all().order_by('date_created')
    return render(request, 'recipes/list_recipes.html', {'recipes': recipes})

#ADD
@permission_required('recipes.add_recipe')
def add_recipe(request):
    if request.method == 'POST':
        form = forms.NewRecipeForm(request)
        try:
            form.save()
        except forms.ValidationError:
            pass
        else:
            return HttpResponseRedirect(reverse('recipes:list'))
    else:
        form = forms.NewRecipeForm()
    return render(request, 'recipes/add.html', {'form': form})

#EDIT
@permission_required('recipes.edit_recipe')
def edit_recipe(request):
    pass


#ACTIVATE
@permission_required('toggle_recipe_is_active')
def activate_recipe(request, recipe_id):
    print('Activating', Recipe.objects.get(id=recipe_id))
    return HttpResponseRedirect(reverse('recipes:list'))

#DEACTIVATE
@permission_required('toggle_recipe_is_active')
def deactivate_recipe(request, recipe_id):
    print('Deactivating', Recipe.objects.get(id=recipe_id))
    return HttpResponseRedirect(reverse('recipes:list'))


# DELETE
@permission_required('recipes.delete_recipe')
def delete_recipe(request):
    pass



# INGEDIENTS ######################################################################################
