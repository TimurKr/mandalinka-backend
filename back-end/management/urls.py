from django.urls import path, include

from management.views.ingredients import IngredientListCreateAPI, IngredientDetailAPI
from management.views.affix import AlergenListAPI, UnitListAPI

urlpatterns = [
    path('ingredients/', IngredientListCreateAPI.as_view(), name='ingredients_api'),
    path('ingredient/<int:pk>/',
         IngredientDetailAPI.as_view(), name='ingredient_detail_api'),
    path('alergens/', AlergenListAPI.as_view(), name='alergens_api'),
    path('units/', UnitListAPI.as_view(), name='units_api'),
]
