# from django.shortcuts import render, redirect

# # from django.urls import reverse
# from django.contrib.auth.decorators import permission_required
# from django.urls import reverse_lazy
# from django.http import HttpResponseBadRequest, JsonResponse, HttpResponse
# from django.core import serializers

# from rest_framework.decorators import api_view
# from rest_framework.response import Response

# from .models import Ingredient, IngredientVersion
# from .forms import NewIngredientForm, IngredientVersionForm
# from .serializers import IngredientSerializer, IngredientVersionSerializer


# def query_ingredients(query, max_results=20):
#     """
#     Returns a queryset of ingredients matching the query.
#     Sorted by:
#     - active ingredients first
#     - usage last month
#     """
#     ingredients = Ingredient.objects.filter(name__unaccent__icontains=query)
#     ingredients = sorted(ingredients, key=lambda ingredient: (
#         ingredient.is_active, ingredient.usage_last_month), reverse=True)
#     return ingredients[:max_results]


# # Views

# @permission_required('ingredients.view_ingredient', login_url=reverse_lazy('recipes:management_page'))
# def management_view(request, new_ingredient_form=None):
#     """Render the management page for ingredients."""

#     if new_ingredient_form is None:
#         new_ingredient_form = NewIngredientForm()
#         is_new_ingredient_modal_active = False
#     else:
#         is_new_ingredient_modal_active = True

#     return render(request, 'ingredients/management.html', {
#         'active_tab': 'ingredients',
#         'new_ingredient_form': new_ingredient_form,
#         'is_new_ingredient_modal_active': is_new_ingredient_modal_active,
#     })


# @permission_required('ingredients.add_ingredient', login_url=reverse_lazy('recipes:management_page'))
# def add_ingredient(request):
#     """View serving POST requests, adds a new ingredient to the database."""
#     if request.method == 'POST':
#         form = NewIngredientForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('ingredients:management_page')
#     else:
#         form = NewIngredientForm()
#     return management_view(request, new_ingredient_form=form)


# # APIs


# @api_view(['GET'])
# @permission_required('ingredients.view_ingredient', login_url=reverse_lazy('recipes:management_page'))
# def search_ingredients(request):
#     """
#     View serving GET requests, returns serialized ingredients matching the query.

#     Allows for GET arguments:
#     - 'q': the search query
#     - 'n': the max number of results to return (default 20)
#     """

#     query = request.GET.get('q')
#     max_results = request.GET.get('n', 20)
#     ingredients = query_ingredients(query, max_results)
#     serializer = IngredientSerializer(
#         ingredients, many=True, context={'request': request})
#     return Response(serializer.data, status=200, content_type='application/json')


# @api_view(['GET'])
# @permission_required('ingredients.view_ingredient', login_url=reverse_lazy('recipes:management_page'))
# def get_ingredient_versions(request):
#     """
#     View serving GET requests, returns all versions on a ingredient (serialized).

#     Required GET arguments:
#     - 'id': ingredient id
#     """
#     try:
#         ingredient = Ingredient.objects.get(pk=request.GET.get('id'))
#     except Ingredient.DoesNotExist:
#         return HttpResponseBadRequest('Ingredient not found')

#     ingredient_versions = ingredient.versions.all()
#     serializer = IngredientVersionSerializer(
#         ingredient_versions, many=True, context={'request': request})
#     return Response(serializer.data, status=200, content_type='application/json')


# @permission_required('ingredients.view_ingredient', login_url=reverse_lazy('recipes:management_page'))
# def ingredient_modal(request, ingredient_id):
#     """
#     View serving GET requests, returns a html div with the modal for an ingredient.

#     Required GET arguments:
#     - 'id': the id of the ingredient to show
#     """
#     try:
#         ingredient = Ingredient.objects.get(id=ingredient_id)
#     except Ingredient.DoesNotExist:
#         return HttpResponseBadRequest('Ingredient not found')

#     return render(request, 'ingredients/info_modal.html', {
#         'ingredient': ingredient
#     })


# @permission_required('ingredients.view_ingredient', login_url=reverse_lazy('recipes:management_page'))
# def ingredient_version_info(request, ingredient_version_id):
#     """
#     View serving GET requests, returns a html div with the version info for an ingredient.

#     Required GET arguments:
#     - 'id': the id of the ingredient to show
#     """
#     try:
#         ingredient_version = IngredientVersion.objects.get(
#             id=ingredient_version_id)
#     except IngredientVersion.DoesNotExist:
#         return HttpResponseBadRequest('Ingredient version not found')

#     return render(request, 'ingredients/version_info.html', {
#         'ingredient_version': ingredient_version,
#     })


# @permission_required('ingredients.add_ingredientversion', login_url=reverse_lazy('recipes:management_page'))
# def new_ingredient_version(request, ingredient_id):
#     """
#     For GET requests returns a div with forms/new_ingredient_version.html
#     For POST request creates a new ingredient version
#     - if succesfull returns success message
#     - if not succesfull returns the form with errors
#     """
#     try:
#         ingredient = Ingredient.objects.get(id=ingredient_id)
#     except IngredientVersion.DoesNotExist:
#         return HttpResponseBadRequest('Ingredient version not found')

#     if request.method == 'POST':
#         form = IngredientVersionForm(
#             ingredient, request.POST, request.FILES)
#         if form.is_valid():
#             new_ingredient = form.save()
#             return render(request, 'ingredients/version_info.html', {
#                 'ingredient': new_ingredient
#             }, status=201)
#         else:
#             return render(request, 'ingredients/forms/new_ingredient_version.html', {
#                 'form': form
#             }, status=406)
#     else:
#         form = IngredientVersionForm(ingredient)
#         return render(request, 'ingredients/forms/new_ingredient_version.html', {
#             'form': form
#         })
