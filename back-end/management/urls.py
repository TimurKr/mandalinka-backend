from django.urls import path, include

from management.views.ingredients import (
    IngredientListCreateAPI,
    IngredientDetailAPI,
    IngredientVersionCreateAPI,
    IngredientVersionModifyAPI)
from management.views.affix import AlergenListAPI, UnitListAPI

urlpatterns = [
    path('ingredients/', IngredientListCreateAPI.as_view(), name='ingredients_api'),
    path('ingredients/<int:pk>/',
         IngredientDetailAPI.as_view(), name='ingredient_detail_api'),
    path('ingredients/<int:pk>/new_version/',
         IngredientVersionCreateAPI.as_view(), name='ingredient_version_api'),
    path('ingredients/versions/<int:pk>/',
         IngredientVersionModifyAPI.as_view(), name='ingredient_version_modify_api'),
    path('alergens/', AlergenListAPI.as_view(), name='alergens_api'),
    path('units/', UnitListAPI.as_view(), name='units_api'),
]
