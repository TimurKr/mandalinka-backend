from typing import Any, Iterable

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.admin.views.decorators import staff_member_required
from django.http import *
from django.urls import reverse, reverse_lazy
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.template import Template, Context
from urllib.parse import urlencode 

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

# RENDER 
@permission_required('recipes.view_recipe')
def render_recipes(request, 
    editing_recipe_id = None,
    messages=[],
    warnings=[], 
    new_recipe_form = None, 
    new_ingredients_formset = None, 
    new_steps_formset = None,
    editing_recipe_forms = None):
    """
    Main page for rendering the recipe tab in management page

    editing_recipe_id: id of the recipe to show when page is loaded
    editing_recipe_forms: dictionary of optional forms to render with the editing_recipe_id
    """

    messages=[]
    warnings=[]
    # Check if the provided editing_recipe_id is valid
    if editing_recipe_id:
        try: 
            Recipe.objects.get(id=editing_recipe_id)
        except:
            warnings.append("Hladaný recept neexistuje")
            editing_recipe_id = None

    # Generate restriction warning if it has been redirected
    redirected_from = request.GET.get('next', None)
    if redirected_from:
        warnings.append('Nedostatočné privilégia')
        if '/add' in redirected_from:
            warnings[-1] += ' na pridanie nového'
        elif '/edit' in redirected_from:
            warnings[-1] += ' na upravenie'
        elif '/activate' in redirected_from:
            warnings[-1] += ' na aktivovanie'
        elif '/deactivate' in redirected_from:
            warnings[-1] += ' na deaktivovanie'
        elif '/retire' in redirected_from:
            warnings[-1] += ' na vypnutie'
        elif '/delete' in redirected_from:
            warnings[-1] += ' na vymazanie'
        warnings[-1] += ' receptu'

    # Create message or a warning if it is in the GET data
    m = request.GET.get('message', None)
    if m:
        messages.append(m)

    # Query all recipes to render
    recipes = {
        Recipe.Statuses.PREPARATION: Recipe.objects.filter(status=Recipe.Statuses.PREPARATION).order_by('date_created'),
        Recipe.Statuses.ACTIVE: Recipe.objects.filter(status=Recipe.Statuses.ACTIVE).order_by('date_created'),
        Recipe.Statuses.RETIRED: Recipe.objects.filter(status=Recipe.Statuses.RETIRED).order_by('date_created'),
    }

    # Add the editinig forms to all recipes
    for recipe in recipes[Recipe.Statuses.PREPARATION]:
        if editing_recipe_id and editing_recipe_id == recipe.id:
            # If editing recipe has been provided and it has id, which is equal to the current recipe
            recipe.edit_general_form = editing_recipe_forms.get('edit_general_form', forms.EditRecipeForm(recipe.id, instance=recipe, prefix=str(recipe.id)))
            recipe.edit_ingredients_formset = editing_recipe_forms.get('edit_ingredients_formset', forms.IngredientInstanceFormset(instance=recipe, prefix=str(recipe.id)))
            recipe.edit_steps_formset = editing_recipe_forms.get('edit_steps_formset', forms.StepFormset(queryset=recipe.steps.order_by('number'), prefix=str(recipe.id)))

        else:
            # If the current recipe is not the editigng recipe provided
            recipe.edit_general_form = forms.EditRecipeForm(recipe.id, instance=recipe, prefix=str(recipe.id))
            recipe.edit_ingredients_formset = forms.IngredientInstanceFormset(instance=recipe, prefix=str(recipe.id))
            recipe.edit_steps_formset = forms.StepFormset(queryset=recipe.steps.order_by('number'), prefix=str(recipe.id))
        
        if not recipe.unique_consecutive_step_numbers() and recipe.edit_steps_formset._non_form_errors == None:
            recipe.edit_steps_formset.full_clean()
            recipe.edit_steps_formset._non_form_errors.append(ValidationError('Nesprávne číslovanie.'))


    # Fill new_recipe_modal if unspecified
    if new_recipe_form or new_ingredients_formset or new_steps_formset:
        is_new_recipe_modal_active = True
    else:
        new_recipe_form = new_recipe_form = forms.NewRecipeForm(initial={'created_by': request.user})
        is_new_recipe_modal_active = False

    return render(request, 'recipes/recipes/main.html', {
        'recipes': recipes,
        'messages': messages,
        'warnings': warnings,
        'name': request.user.first_name,
        'active_tab': 'recipes',
        'new_recipe_form': new_recipe_form,
        'new_ingredients_formset': new_ingredients_formset,
        'new_steps_formset': new_steps_formset,
        'is_new_recipe_modal_active': is_new_recipe_modal_active,
        'editing_recipe_id': editing_recipe_id,
    })

@permission_required('recipes.view_recipe')
def recipe_info(request, recipe_id):
    # Redirect if not GET
    if request.method != 'GET':
        return HttpResponseRedirect(reverse('recipes:render_editing_recipe', args=(recipe_id,)))

    # Redirect if recipe doesn't exist
    try: 
        recipe = Recipe.objects.get(id=recipe_id)
    except:
        return HttpResponseRedirect(reverse('recipes:render_recipes'))

    return render(request, 'recipes/recipes/info_widget.html', {'recipe': recipe})
    



# ADD
@permission_required('recipes.add_recipe', login_url='recipes:render_recipes')
def add_recipe(request):
    if request.method == 'POST':
        form = forms.NewRecipeForm(request.POST)
        try:
            new_recipe = form.save()
            if new_recipe.created_by.id != request.user.id and not request.user.is_superuser:
                form.add_error('created_by', ValidationError(f'Nemáte povolenie pridávať recepty pod iným menom. Momentálne ste prihlásený ako {request.user.get_full_name()}', 'insufficient_permissions'))
                raise ValueError('Nemáte povolenie pridávať recepty pod iným ako vlastným menom.', 'insufficient_permissions')
        except Exception as e:
            print(e)
        else:
            return HttpResponseRedirect(reverse('recipes:add_recipe_ingredients', args=(new_recipe.id,)))
    else:
        form = forms.NewRecipeForm(initial={'created_by': request.user})
    return render_recipes(request, new_recipe_form = form)

@permission_required('recipes.add_recipe', login_url='recipes:render_recipes')
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

    return render_recipes(request, new_recipe_form = form)

@permission_required('recipes.add_recipe', login_url='recipes:render_recipes')
def add_recipe_ingredients(request, recipe_id):
    try:
        recipe = Recipe.objects.get(id=recipe_id)
    except:
        return HttpResponseRedirect(reverse('recipes:render_recipes'))

    if request.method == 'POST': 
        formset = forms.IngredientInstanceFormset(request.POST, request.FILES, recipe, prefix=str(recipe.id))

        if formset.is_valid():
            formset.save()
            if request.POST.get('ingredients_finished', False):
                recipe.ingredients_finished = True
                recipe.save()
            else:
                recipe.ingredients_finished = False
                recipe.save()
            return HttpResponseRedirect(reverse('recipes:add_recipe_steps', args=(recipe.id,)))

    else:
        formset = forms.IngredientInstanceFormset(instance=recipe, prefix=str(recipe.id))
    return render_recipes(request, new_ingredients_formset = formset)

@permission_required('recipes.add_recipe', login_url='recipes:render_recipes')
def add_recipe_steps(request, recipe_id):
    try:
        recipe = Recipe.objects.get(id=recipe_id)
    except:
        return HttpResponseRedirect(reverse('recipes:render_recipes'))

    if request.method == 'POST': 
        formset = forms.StepFormset(request.POST, request.FILES, queryset=recipe.steps.order_by('number'), prefix=str(recipe.id))

        if formset.is_valid():
            steps = formset.save(commit=False)         
            for step in steps:
                step.recipe = recipe
                step.save()

            print(recipe.steps.count())

            # Success - New recipe done
            if recipe.unique_consecutive_step_numbers():
                if request.POST.get('steps_finished', False):
                    recipe.steps_finished = True
                    recipe.save()
                else:
                    recipe.steps_finished = False
                    recipe.save()

                return redirect(reverse('recipes:render_recipes') + 
                    '?' + urlencode({'message': f"Nový recept {recipe.name} úspešne vytvorený"}))              
            
            recipe.steps.all().delete()
            formset._non_form_errors.append(ValidationError('Nesprávne číslovanie.'))
            recipe.steps_finished = False
            recipe.save()

    else:
        formset = forms.StepFormset(queryset=recipe.steps.order_by('number'), prefix=str(recipe.id))
        if not recipe.unique_consecutive_step_numbers():
            formset._non_form_errors.append(ValidationError('Nesprávne číslovanie.'))

    # Formset is invalid
    return render_recipes(request, new_steps_formset=formset)
 

# EDIT
@permission_required('recipes.change_recipe')
def render_editing_recipe(request, editing_recipe_id):
    """
    View for GET request of an editing view of a particular recipe
    """
    if request.method == 'GET':
        return render_recipes(request, editing_recipe_id=editing_recipe_id)
    else:
        return HttpResponseBadRequest()

@permission_required('recipes.change_recipe', login_url='recipes:render_recipes')
def edit_recipe_general(request, recipe_id):
    """
    View serving only for POSTing general recipe form data
    """
    # Redirect if not POST
    if request.method != 'POST':
        return HttpResponseRedirect(reverse('recipes:render_editing_recipe', args=(recipe_id,)))

    # Redirect if recipe doesn't exist
    try: 
        recipe = Recipe.objects.get(id=recipe_id)
    except:
        return HttpResponseRedirect(reverse('recipes:render_recipes'))

    # Process the form data
    general_form = forms.EditRecipeForm(recipe_id, request.POST, request.FILES, instance=recipe)
    try:
        general_form.save()
    except:
        # Form didn't validate
        return render_recipes(request, editing_recipe_id=recipe_id, editing_recipe_forms={'edit_general_form': general_form})
    else:
        # Success
        return render_recipes(request, editing_recipe_id=recipe_id)

@permission_required('recipes.change_recipe', login_url='recipes:render_recipes')
def edit_recipe_steps(request, recipe_id):
    """
    View serving only for POSTing recipe steps formset data
    """
    # Redirect if not POST
    if request.method != 'POST':
        return HttpResponseRedirect(reverse('recipes:render_editing_recipe', args=(recipe_id,)))

    # Redirect if recipe doesn't exist
    try: 
        recipe = Recipe.objects.get(id=recipe_id)
    except:
        return HttpResponseRedirect(reverse('recipes:render_recipes'))

    formset = forms.StepFormset(request.POST, request.FILES, queryset=recipe.steps.order_by('number'), prefix=str(recipe.id))

    if formset.is_valid():
        steps = formset.save(commit=False)
        for step in steps:
            step.recipe = recipe
            step.save()

        if recipe.unique_consecutive_step_numbers():
            # Success
            return render_recipes(request, editing_recipe_id=recipe_id)
        else:
            # Steps aren't consecutive
            formset._non_form_errors.append(ValidationError('Nesprávne číslovanie.'))
            recipe.steps_finished = False
            recipe.save()

    return render_recipes(request, editing_recipe_id=recipe_id, editing_recipe_forms={'edit_steps_form': formset})
    

@permission_required('recipes.change_recipe', login_url='recipes:render_recipes')
def edit_recipe_ingredients(request, recipe_id):
    """
    View serving only for POSTing recipe ingredients formset data
    """
    # Redirect if not POST
    if request.method != 'POST':
        return HttpResponseRedirect(reverse('recipes:render_editing_recipe', args=(recipe_id,)))

    # Redirect if recipe doesn't exist
    try: 
        recipe = Recipe.objects.get(id=recipe_id)
    except:
        return HttpResponseRedirect(reverse('recipes:render_recipes'))

    formset = forms.IngredientInstanceFormset(request.POST, request.FILES, recipe, prefix=str(recipe.id))

    if formset.is_valid():
        # Success
        formset.save()
        return render_recipes(request, editing_recipe_id=recipe_id)
    else:
        return render_recipes(request, editing_recipe_id=recipe_id, editing_recipe_forms={'edit_ingredients_form': formset})



# ACTIVATE
@permission_required('recipes.toggle_recipe_status', login_url='recipes:render_recipes')
def activate_recipe(request, recipe_id):
    Recipe.objects.get(id=recipe_id).activate()
    return HttpResponseRedirect(reverse('recipes:render_recipes'))

# DEACTIVATE
@permission_required('recipes.toggle_recipe_status', login_url='recipes:render_recipes')
def deactivate_recipe(request, recipe_id):
    Recipe.objects.get(id=recipe_id).deactivate()
    return HttpResponseRedirect(reverse('recipes:render_recipes'))

# RETIRE
@permission_required('recipes.toggle_recipe_status', login_url='recipes:render_recipes')
def retire_recipe(request, recipe_id):
    Recipe.objects.get(id=recipe_id).retire()
    return HttpResponseRedirect(reverse('recipes:render_recipes'))


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
        except ValueError as e:
            pass
        else:
            if 'aktivovať' in request.POST['submit']:
                ingredient.activate()
            ingredient.save()
            form.save_m2m()
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
            ingredient.save()
            form.save_m2m()
            return HttpResponseRedirect(reverse('recipes:list_ingredients'))
    else:
        form = forms.EditIngredientForm(ingredient_id, instance=ingredient)
    return render(request,"recipes/ingredients/edit.html", {'form':form})



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

