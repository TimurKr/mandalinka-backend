from django.urls import path

from management.views.ingredients import IngredientListCreateAPI, IngredientDetailAPI

urlpatterns = [
    path('ingredients/', IngredientListCreateAPI.as_view(), name='ingredients_api'),
    path('ingredient/<int:pk>/',
         IngredientDetailAPI.as_view(), name='ingredient_detail_api'),
]
