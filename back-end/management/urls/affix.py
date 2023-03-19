from django.urls import path, include


from management.views.affix import AlergenListAPI, UnitListAPI, AttributeListAPI, DietListAPI, KitchenListAPI


urlpatterns = [

    ### AFFIXES ###
    path('units/', UnitListAPI.as_view(), name='units_api'),
    path('alergens/', AlergenListAPI.as_view(), name='alergens_api'),
    path('attributes/', AttributeListAPI.as_view(), name='attributes_api'),
    path('diets/', DietListAPI.as_view(), name='diets_api'),
    path('kitchen-accesories/', KitchenListAPI.as_view(),
         name='kitchen_accesories_api'),

]
