from django.urls import path

from . import views

app_name = 'recipes'

urlpatterns = [
    path('recipe/list', views.list_recipes, name='list_recipes'), 
    path('recipe/activate/<recipe_id>', views.activate_recipe, name='activate_recipe'),
    path('recipe/deactivate/<recipe_id>', views.deactivate_recipe, name='deactivate_recipe'),
    path('recipe/delete/<recipe_id>', views.delete_recipe, name='delete_recipe'),

    # path('ingredients/list', views.list_ingredients, name='list_ingredients'),
    # path('ingredients/activate/<ingredient_id>', views.activate_ingredient, name='activate_ingredient'),
    # path('ingredients/deactivate/<ingredient_id>', views.deactivate_ingredient, name='deactivate_ingredient'),
    
]