from django.urls import path

from management.views import ingredients as views

urlpatterns = [

    ### INGREDIENTS ###

    # List, create

    path('', views.IngredientListCreateAPI.as_view(),
         name='ingredients_api'),
    # Retrieve, update
    path('<int:pk>/',
         views.IngredientRetrieveUpdateAPI.as_view(), name='ingredient_detail_api'),


    ### INGREDIENT VERSIONS ###

    # Create
    path('new_version/',
         views.IngredientVersionCreateAPI.as_view(), name='ingredient_version_api'),
    # Retrieve, update, delete
    path('versions/<int:pk>/',
         views.IngredientVersionRetrieveUpdateDestroyAPI.as_view(), name='ingredient_version_modify_api'),


    ### INGREDIENT VERSION STOCK ###

    ## Removals ##
    # Create ingredient stock removal
    path('new_stock_removal/',
         views.IngredientVersionStockRemovalCreateAPI.as_view(), name='ingredient_version_remove_stock_api'),
    # Delete ingredient stock removal with given id
    path('stock_removals/<int:pk>/',
         views.IngredientVersionStockRemovalDeleteAPI.as_view(), name='ingredient_version_remove_stock_modify_api'),

    ## Orders ##
    # Create ingredient stock order
    path('new_stock_order/',
         views.IngredientVersionStockOrderCreateAPI.as_view(), name='ingredient_version_order_stock_api'),
    # Delete ingredient stock order
    path('stock_orders/<int:pk>/',
         views.IngredientVersionStockOrderModifyAPI.as_view(), name='ingredient_version_order_stock_modify_api'),

]
