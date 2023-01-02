from django.urls import path

from . import views

app_name = 'recipes'

urlpatterns = [
    path('', views.recipes_management_view, name='manage'),

    path('recipes/list', views.list_recipes, name='list_recipes'), 
    path('recipe/add', views.add_recipe, name='add_recipe'),
    path('recipe/add/<predecessor_id>', views.add_recipe_descendant, name='add_recipe_descendant'),
    path('recipe/edit/<recipe_id>', views.edit_recipe, name='edit_recipe'),
    path('recipe/edit/ingrediences/<recipe_id>', views.edit_recipe_ingrediences, name='edit_recipe_ingrediences'),
    path('recipe/activate/<recipe_id>', views.activate_recipe, name='activate_recipe'),
    path('recipe/deactivate/<recipe_id>', views.deactivate_recipe, name='deactivate_recipe'),
    path('recipe/delete/<recipe_id>', views.delete_recipe, name='delete_recipe'),

    path('ingredients/list', views.list_ingredients, name='list_ingredients'),
    path('ingredient/add', views.add_ingredient, name='add_ingredient'),
    path('ingredient/edit/<ingredient_id>', views.edit_ingredient, name='edit_ingredient'),
    path('ingredient/activate/<ingredient_id>', views.activate_ingredient, name='activate_ingredient'),
    path('ingredient/deactivate/<ingredient_id>', views.deactivate_ingredient, name='deactivate_ingredient'),
    path('ingredient/delete/<ingredient_id>', views.delete_ingredient, name='delete_ingredient'),

    path('alergens/list', views.list_alergens, name='list_alergens'),
    path('alergen/add', views.add_alergen, name='add_alergen'),
    
]