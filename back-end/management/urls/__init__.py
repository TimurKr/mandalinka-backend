from django.urls import path, include

urlpatterns = [
    ### AFFIXES ###
    path('', include('management.urls.affix')),

    ### INGREDIENTS ###
    path('ingredients/', include('management.urls.ingredients')),

    ### RECIPE DESIGNS ###
    path('recipe-designs/', include('management.urls.recipe_designs')),

]
