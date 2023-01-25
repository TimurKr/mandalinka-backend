from django.urls import path

from . import views

app_name = 'ingredients'

urlpatterns = [
    path('', views.management_view, name='management_page'),
    
    ### API ###
    path('api/search/', views.search_ingredients, name='search_ingredients'),
    path('api/get-ingredient-modal/<ingredient_id>', views.ingredient_modal, name='ingredient_modal'),
    path('api/get-ingredient-version-info/<ingredient_version_id>', views.ingredient_version_info, name='ingredient_version_info'),
    path('api/new-ingredient-version/<ingredient_id>', views.new_ingredient_version, name='new_ingredient_version'),

    path('add/', views.add_ingredient, name='add'),

]