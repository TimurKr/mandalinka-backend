from django.urls import path
from . import views

app_name = 'recipes'

urlpatterns = [
    path('', views.management_view, name='management_page'),

    ### RECIPES ###
    # RENDER
    path('<recipe_id>/info/', views.info_widget, name='recipe_widget'), 
    path('<recipe_id>/edit/', views.edit_widget, name='edit_widget'), 
    path('load_more/', views.load_more, name='load_more_recipes'),
    # ADD
    path('add/', views.add, name='add'),
    path('add/<predecessor_id>/', views.add_descendant, name='add_descendant'),
    # EDIT
    path('<recipe_id>/edit/general/', views.edit_general, name='edit_general'), # post
    path('<recipe_id>/edit/steps/', views.edit_steps, name='edit_steps'), # post
    path('<recipe_id>/edit/ingredients/', views.edit_ingredients, name='edit_ingredients'), # post
    # EDIT_STATUS
    path('<recipe_id>/activate/', views.activate, name='activate'),
    path('<recipe_id>/deactivate/', views.deactivate, name='deactivate'),
    path('<recipe_id>/retire/', views.retire, name='retire'),

]