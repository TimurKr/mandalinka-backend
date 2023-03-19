from django.urls import path

from management.views import recipe_designs as views

urlpatterns = [

    ### RECIPE DESIGNS ###
    # Create and list recipe designs
    path('', views.RecipeDesignListCreateAPI.as_view(),
         name='recipe_designs_api'),

]
