from django.shortcuts import render, redirect

# from django.urls import reverse
from django.contrib.auth.decorators import permission_required
from django.urls import reverse_lazy

from .models import Ingredient
from .forms import NewIngredientForm

# Create your views here.

@permission_required('ingredients.view_ingredient', login_url=reverse_lazy('recipes:management_page'))
def management_view(request, new_ingredient_form=None):
    """Render the management page for ingredients."""

    if new_ingredient_form is None:
        new_ingredient_form = NewIngredientForm()
        is_new_ingredient_modal_active = False
    else:
        is_new_ingredient_modal_active = True

    return render(request, 'ingredients/management.html', {
        'active_tab': 'ingredients',
        'ingredients': query_ingredients(''),
        'new_ingredient_form': new_ingredient_form,
        'is_new_ingredient_modal_active': is_new_ingredient_modal_active,
    })


def query_ingredients(query, max_results=20):
    """
    Returns a queryset of ingredients matching the query.
    Sorted by:
    - active ingredients first
    - usage last month
    """
    ingredients = Ingredient.objects.filter(name__unaccent__icontains=query)
    ingredients = sorted (ingredients, key=lambda ingredient: (ingredient.active, ingredient.usage_last_month), reverse=True)
    return ingredients[:max_results]


@permission_required('ingredients.view_ingredient', login_url=reverse_lazy('recipes:management_page'))
def search_ingredients(request):
    """
    View serving GET requests, returns a html div with the search result list of ingredients.

    Allows for GET arguments:
    - 'q': the search query
    - 'n': the max number of results to return (default 20)
    """
    return render(request, 'ingredients/search_results.html', {
        'ingredients': query_ingredients(request.GET.get('q', ''), request.GET.get('n', 20))
        })

@permission_required('ingredients.add_ingredient', login_url=reverse_lazy('recipes:management_page'))
def add_ingredient(request):
    """View serving POST requests, adds a new ingredient to the database."""
    if request.method == 'POST':
        form = NewIngredientForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('ingredients:management_page')
    else:
        form = NewIngredientForm()
    return management_view(request, new_ingredient_form=form)