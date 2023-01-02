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
        if '/ingredients/list' in redirected_from or \
            '/recipes/list' in redirected_from or \
            '/alergens/list' in redirected_from:
            warning = 'Nedostatočné privilégia'

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
        if '/add' in redirected_from:
            warning += ' na pridanie nového'
        elif '/edit' in redirected_from:
            warning += ' na upravenie'
        elif '/activate' in redirected_from:
            warning += ' na aktivovanie'
        elif '/deactivate' in redirected_from:
            warning += ' na deaktivovanie'
        elif '/delete' in redirected_from:
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
            form.is_valid()
            if form.cleaned_data['created_by'] != request.user and not request.user.is_superuser:
                form.add_error('created_by', ValidationError(f'Nemáte povolenie pridávať recepty pod iným menom. Momentálne ste prihlásený ako {request.user.get_full_name()}', 'insufficient_permissions'))
                raise ValueError('Nemáte povolenie pridávať recepty pod iným ako vlastným menom.', 'insufficient_permissions')
            new_recipe = form.save()
        except ValueError as e:
            print(e)
            print(form.errors.as_data())
            pass
        else:
            return HttpResponseRedirect(reverse('recipes:edit_recipe_ingrediences', args=(new_recipe.id, )))
    else:
        form = forms.NewRecipeForm(initial={'created_by': request.user})
    return render(request, 'recipes/recipes/add.html', {'form': form})


@permission_required('recipes.add_recipe', login_url='recipes:list_recipes')
def add_recipe_descendant(request, predecessor_id):
    if request.method != 'GET':
        return HttpResponseBadRequest(request)

    try:
        predecessor = Recipe.objects.get(id=predecessor_id)
    except:
        return HttpResponseBadRequest(request)

    form = forms.NewRecipeForm(
        initial = {
            'predecessor': predecessor,
            'created_by': request.user,
            }, 
        instance = predecessor)

    return render(request, 'recipes/recipes/add.html', {'form': form})


# EDIT TODO:
@permission_required('recipes.change_recipe', login_url='recipes:list_recipes')
def edit_recipe(request, recipe_id):
    return list_recipes(request)

@permission_required('recipes.add_recipe', login_url='recipes:list_recipes')
def edit_recipe_ingrediences(request, recipe_id):
    if request.method == 'POST':
        pass
    else:
        formset = forms.IngredientInstanceFormset(instance=Recipe.objects.get(id=recipe_id))
    return render(request, 'recipes/recipes/edit_ingrediences.html', {
            'formset': formset,
            "recipe_id": recipe_id
            })


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
@permission_required('recipes.view_ingredient', login_url='recipes:manage')
def list_ingredients(request):

    redirected_from = request.GET.get('next', None)
    warning = None
    if redirected_from:
        warning = 'Nedostatočné privilégia'
        if '/add' in redirected_from:
            warning += ' na pridanie novej'
        elif '/edit' in redirected_from:
            warning += ' na upravenie'
        elif '/activate' in redirected_from:
            warning += ' na aktivovanie'
        elif '/deactivate' in redirected_from:
            warning += ' na deaktivovanie'
        elif '/delete' in redirected_from:
            warning += ' na vymazanie'
        warning += ' ingrediencie'
    
    ingredients = {
        'active': Ingredient.objects.filter(is_active=True),
        'inactive': Ingredient.objects.filter(is_active=False),
    }
    return render(request, 'recipes/ingredients/list.html', {
            'warning': warning,
            'ingredients': ingredients,
        })


# ADD
@permission_required('recipes.add_ingredient', login_url='recipes:list_ingredients')
def add_ingredient(request):
    if request.method == 'POST':
        form = forms.NewIngredientForm(request.POST)
        try:
            ingredient = form.save(commit=False)
            if 'aktivovať' in request.POST['submit']:
                ingredient.activate()
        except ValueError as e:
            pass
        else:
            ingredient.save()
            return HttpResponseRedirect(reverse('recipes:list_ingredients'))
    else:
        form = forms.NewIngredientForm(initial={'created_by': request.user.id})
    return render(request, 'recipes/ingredients/add.html', {'form': form})


# EDIT
@permission_required('recipes.change_ingredient', login_url='recipes:list_ingredients')
def edit_ingredient(request, ingredient_id):
    try:
        ingredient = Ingredient.objects.get(id=ingredient_id)
    except:
        return HttpResponseRedirect(reverse('recipes:list_ingredients'))

    if request.method == 'POST':
        form = forms.EditIngredientForm(ingredient_id, request.POST, instance=ingredient)
        try:
            ingredient = form.save(commit=False)
        except ValueError:
            pass
        else:
            if 'aktivovať' in request.POST['submit']:
                ingredient.activate()
            form.save_m2m()
            ingredient.save()
            return HttpResponseRedirect(reverse('recipes:list_ingredients'))
    else:
        form = forms.EditIngredientForm(ingredient_id, instance=ingredient)
    return render(request,"recipes/ingredients/edit.html", {'form':form})


    if request.method == 'POST':
        form = forms.IngredientForm(request.POST)
        form.helper.form_action = reverse_lazy('recipes:edit_ingredient')
        try:
            i = form.save(commit=False)
            if 'aktivovať' in request.POST['submit']:
                i.activate()
        except ValueError as e:
            print(e)
            print(form.errors.as_data())
            pass
        else:
            i.save()
            return HttpResponseRedirect(reverse('recipes:list_ingredients'))
    else:
        form = forms.IngredientForm(instance=Ingredient)
    return render(request, 'recipes/ingredients/add.html', {'form': form})


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
@permission_required('recipes.view_alergen', login_url='recipes:manage')
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