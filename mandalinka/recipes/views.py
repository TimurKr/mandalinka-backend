from django.shortcuts import render

from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.admin.views.decorators import staff_member_required
from django.http import *
from django.urls import reverse, reverse_lazy
from django.core.exceptions import ValidationError

from .models import Recipe, Ingredient
from . import forms

import datetime

# GENERAL ######################################################################################

@staff_member_required(login_url="customers:home_page")
def recipes_management_view(request):
    redirected_from = request.GET.get('next', None)
    warning = None
    if redirected_from:
        warning = 'Nedostatočné privilégia'
        if redirected_from.find('/add') != -1:
            warning += ' na pridanie nového'
        elif redirected_from.find('/edit') != -1:
            warning += ' na upravenie'
        elif redirected_from.find('/activate') != -1:
            warning += ' na aktivovanie'
        elif redirected_from.find('/deactivate') != -1:
            warning += ' na deaktivovanie'
        elif redirected_from.find('/delete') != -1:
            warning += ' na vymazanie'
        warning += ' receptu'
    return render(request, 'recipes/manage.html', {
            "warning": warning,
            "name": request.user.first_name,
        })


# RECIPES ######################################################################################

# LIST
@permission_required('recipes.view_recipe')
def list_recipes(request):

    redirected_from = request.GET.get('next', None)
    warning = None
    if redirected_from:
        warning = 'Nedostatočné privilégia'
        if redirected_from.find('/add') != -1:
            warning += ' na pridanie nového'
        elif redirected_from.find('/edit') != -1:
            warning += ' na upravenie'
        elif redirected_from.find('/activate') != -1:
            warning += ' na aktivovanie'
        elif redirected_from.find('/deactivate') != -1:
            warning += ' na deaktivovanie'
        elif redirected_from.find('/delete') != -1:
            warning += ' na vymazanie'
        warning += ' receptu'


    recipes = {
        'recent': Recipe.objects.filter(date_created__gte=datetime.date.today() - datetime.timedelta(days=7), is_active=False),
        'active': Recipe.objects.filter(is_active=True), 
        'inactive': Recipe.objects.filter(is_active=False)
    }
    return render(request, 'recipes/recipes/list.html', {
            'recipes': recipes,
            'warning': warning,
        })


# ADD
@permission_required('recipes.add_recipe', login_url='recipes:list_recipes')
def add_recipe(request):
    if request.method == 'POST':
        form = forms.NewRecipeForm(request.POST)
        try:
            form.save()
            if form.cleaned_data['created_by'] != request.user and not request.user.is_superuser:
                form.add_error('created_by', ValidationError('Nemáte povolenie pridávať recepty pod iným menom.', 'insufficient_permissions'))
                raise Exception()
        except ValueError as e:
            print(e)
            print(form.errors.as_data())
            pass
        else:
            return HttpResponseRedirect(reverse('recipes:list_recipes'))
    else:
        form = forms.NewRecipeForm(initial={'created_by': request.user.id})
    return render(request, 'recipes/recipes/add.html', {'form': form})


# EDIT TODO:
@permission_required('recipes.change_recipe', login_url='recipes:list_recipes')
def edit_recipe(request, recipe_id):
    return list_recipes(request)


# ACTIVATE
@permission_required('recipes.toggle_is_active_recipe', login_url='recipes:list_recipes')
def activate_recipe(request, recipe_id):
    Recipe.objects.get(id=recipe_id).activate()
    return HttpResponseRedirect(reverse('recipes:list_recipes'))


# DEACTIVATE
@permission_required('recipes.toggle_is_active_recipe', login_url='recipes:list_recipes')
def deactivate_recipe(request, recipe_id):
    Recipe.objects.get(id=recipe_id).deactivate()
    return HttpResponseRedirect(reverse('recipes:list_recipes'))


# DELETE TODO:
@permission_required('recipes.delete_recipe', login_url='recipes:list_recipes')
def delete_recipe(request):
    pass



# INGEDIENTS ######################################################################################

# LIST
@permission_required('recipes.view_ingredient')
def list_ingredients(request):

    redirected_from = request.GET.get('next', None)
    warning = None
    if redirected_from:
        warning = 'Nedostatočné privilégia'
        if redirected_from.find('/add') != -1:
            warning += ' na pridanie novej'
        elif redirected_from.find('/edit') != -1:
            warning += ' na upravenie'
        elif redirected_from.find('/activate') != -1:
            warning += ' na aktivovanie'
        elif redirected_from.find('/deactivate') != -1:
            warning += ' na deaktivovanie'
        elif redirected_from.find('/delete') != -1:
            warning += ' na vymazanie'
        warning += ' ingrediencie'
    
    ingredients = Ingredient.objects.all()

    return render(request, 'recipes/ingredients/list.html', {
            'warning': warning,
            'ingredients': ingredients,
        })


# ADD
@permission_required('recipes.add_ingredient', login_url='recipes:list_ingredients')
def add_ingredient(request):
    # if request.method == 'POST':
    #     form = forms.NewRecipeForm(request.POST)
    #     try:
    #         form.save()
    #         if form.cleaned_data['created_by'] != request.user and not request.user.is_superuser:
    #             form.add_error('created_by', ValidationError('Nemáte povolenie pridávať recepty pod iným menom.', 'insufficient_permissions'))
    #             raise Exception()
    #     except ValueError as e:
    #         print(e)
    #         print(form.errors.as_data())
    #         pass
    #     else:
    #         return HttpResponseRedirect(reverse('recipes:list_recipes'))
    # else:
    #     form = forms.NewRecipeForm(initial={'created_by': request.user.id})
    return render(request, 'recipes/ingredients/add.html')


# EDIT
@permission_required('recipes.change_ingredient', login_url='recipes:list_ingredients')
def edit_ingredient(request):
    pass


# ACTIVATE
@permission_required('recipes.toggle_is_active_ingredient', login_url='recipes:list_ingredients')
def activate_ingredient(request, ingredient_id):
    Ingredient.objects.get(id=ingredient_id).activate()
    return HttpResponseRedirect(reverse('recipes:list_ingredients'))


# DEACTIVATE
@permission_required('recipes.toggle_is_active_ingredient', login_url='recipes:list_ingredients')
def deactivate_ingredient(request, ingredient_id):
    Ingredient.objects.get(id=ingredient_id).deactivate()
    return HttpResponseRedirect(reverse('recipes:list_ingredients'))


# DELETE
@permission_required('recipes.delete_ingredient', login_url='recipes:list_ingredients')
def delete_ingredient(request):
    pass


# ALERGENS ######################################################################################

# LIST
@permission_required('recipes.view_alergens')
def list_alergens(request):

    redirected_from = request.GET.get('next', None)
    warning = None
    if redirected_from:
        warning = 'Nedostatočné privilégia'
        if redirected_from.find('/add') != -1:
            warning += ' na pridanie nového'
        elif redirected_from.find('/edit') != -1:
            warning += ' na upravenie'
        elif redirected_from.find('/activate') != -1:
            warning += ' na aktivovanie'
        elif redirected_from.find('/deactivate') != -1:
            warning += ' na deaktivovanie'
        elif redirected_from.find('/delete') != -1:
            warning += ' na vymazanie'
        warning += ' alergénu'

    return render(request, 'recipes/alergens/list.html', {
            'warning': warning,
        })


# ADD
@permission_required('recipes.add_alergen', login_url='recipes:list_alergens')
def add_alergen(request):
    # if request.method == 'POST':
    #     form = forms.NewRecipeForm(request.POST)
    #     try:
    #         form.save()
    #         if form.cleaned_data['created_by'] != request.user and not request.user.is_superuser:
    #             form.add_error('created_by', ValidationError('Nemáte povolenie pridávať recepty pod iným menom.', 'insufficient_permissions'))
    #             raise Exception()
    #     except ValueError as e:
    #         print(e)
    #         print(form.errors.as_data())
    #         pass
    #     else:
    #         return HttpResponseRedirect(reverse('recipes:list_recipes'))
    # else:
    #     form = forms.NewRecipeForm(initial={'created_by': request.user.id})
    return render(request, 'recipes/alergens/add.html')