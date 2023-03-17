from django.urls import path, include

from management.views import ingredients as views

from management.views.affix import AlergenListAPI, UnitListAPI

urlpatterns = [

    ### INGREDIENTS ###

    # List, create
    path('ingredients/', views.IngredientListCreateAPI.as_view(),
         name='ingredients_api'),
    # Retrieve, update
    path('ingredients/<int:pk>/',
         views.IngredientRetrieveUpdateAPI.as_view(), name='ingredient_detail_api'),


    ### INGREDIENT VERSIONS ###

    # Create
    path('ingredients/new_version/',
         views.IngredientVersionCreateAPI.as_view(), name='ingredient_version_api'),
    # Retrieve, update, delete
    path('ingredients/versions/<int:pk>/',
         views.IngredientVersionRetrieveUpdateDestroyAPI.as_view(), name='ingredient_version_modify_api'),


    ### INGREDIENT VERSION STOCK ###

    ## Removals ##
    # Create ingredient stock removal
    path('ingredients/new_stock_removal/',
         views.IngredientVersionStockRemovalCreateAPI.as_view(), name='ingredient_version_remove_stock_api'),
    # Delete ingredient stock removal with given id
    path('ingredients/stock_removals/<int:pk>/',
         views.IngredientVersionStockRemovalDeleteAPI.as_view(), name='ingredient_version_remove_stock_modify_api'),

    ## Orders ##
    # Create ingredient stock order
    path('ingredients/new_stock_order/',
         views.IngredientVersionStockOrderCreateAPI.as_view(), name='ingredient_version_order_stock_api'),
    # Delete ingredient stock order
    path('ingredients/stock_orders/<int:pk>/',
         views.IngredientVersionStockOrderModifyAPI.as_view(), name='ingredient_version_order_stock_modify_api'),


    ### AFFIXES ###

    path('alergens/', AlergenListAPI.as_view(), name='alergens_api'),
    path('units/', UnitListAPI.as_view(), name='units_api'),
]
