from django.urls import path

from management.views.ingredients import IngredientListCreate, IngredientDetail

urlpatterns = [
    path('ingredients/', IngredientListCreate.as_view(), name='ingredients'),
    path('ingredients/<int:pk>/', IngredientDetail.as_view(),
         name='ingredient-detail'),
]
