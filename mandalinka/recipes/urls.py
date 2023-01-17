from django.urls import path

from . import views

app_name = 'recipes'

urlpatterns = [
    path('', views.recipes_management_view, name='manage'),

    ### RECIPES ###
    # RENDER
    path('recipes/', views.render_recipes, name='render_recipes'), 
    path('recipe/info/<recipe_id>/', views.recipe_info_widget, name='recipe_info_widget'), 
    path('recipe/edit/<recipe_id>/', views.recipe_edit_widget, name='recipe_edit_widget'), 
    path('recipes/load_more/', views.load_more_recipes, name='load_more_recipes'),
    # ADD
    path('recipe/add/', views.add_recipe, name='add_recipe'),
    path('recipe/add/<predecessor_id>/', views.add_recipe_descendant, name='add_recipe_descendant'),
    # EDIT
    path('recipe/edit/<recipe_id>/general/', views.edit_recipe_general, name='edit_recipe_general'), # post
    path('recipe/edit/<recipe_id>/steps/', views.edit_recipe_steps, name='edit_recipe_steps'), # post
    path('recipe/edit/<recipe_id>/ingredients/', views.edit_recipe_ingredients, name='edit_recipe_ingredients'), # post
    # EDIT_STATUS
    path('recipe/activate/<recipe_id>/', views.activate_recipe, name='activate_recipe'),
    path('recipe/deactivate/<recipe_id>/', views.deactivate_recipe, name='deactivate_recipe'),
    path('recipe/retire/<recipe_id>/', views.retire_recipe, name='retire_recipe'),

    ### INGREDIENTS ###
    path('ingredients/list/', views.list_ingredients, name='list_ingredients'),
    path('ingredient/add/', views.add_ingredient, name='add_ingredient'),
    path('ingredient/edit/<ingredient_id>/', views.edit_ingredient, name='edit_ingredient'),
    path('ingredient/activate/<ingredient_id>/', views.activate_ingredient, name='activate_ingredient'),
    path('ingredient/deactivate/<ingredient_id>/', views.deactivate_ingredient, name='deactivate_ingredient'),
]