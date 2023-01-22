from django.urls import path

from . import views

app_name = 'ingredients'

urlpatterns = [
    path('', views.management_view, name='management_page'),
    
    ### API ###
    path('search/', views.search_ingredients, name='search_ingredients'),
    

    path('add/', views.add_ingredient, name='add'),

]