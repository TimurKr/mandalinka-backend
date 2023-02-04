from django.urls import path

from management.views.ingredients import IngredientListCreate, IngredientDetail

urlpatterns = [
    path('list', IngredientListCreate.as_view(), name='ingredients_list'),
    path('add', IngredientListCreate.as_view(), name='ingredients_list'),
    path('<int:pk>/', IngredientDetail.as_view(),
         name='ingredient-detail'),
]
