from django.contrib import admin

# Register your models here.

from .affix.models import Attribute, Alergen, Diet, KitchenAccesory
from .ingredients.models import (
    Ingredient,
    IngredientVersion,
    IngredientVersionStockChange,
    IngredientVersionStockOrder,
    IngredientVersionStockRemove
)
from .recipe_designs.models import RDStep, RDError, RDIngredient, RecipeDesign
from .menus.models import RMIngredient, RecipeInMenu, Menu

admin.site.register(Attribute)
admin.site.register(Alergen)
admin.site.register(Diet)
admin.site.register(KitchenAccesory)
admin.site.register(Ingredient)
admin.site.register(IngredientVersion)
admin.site.register(IngredientVersionStockChange)
admin.site.register(IngredientVersionStockOrder)
admin.site.register(IngredientVersionStockRemove)
admin.site.register(RDStep)
admin.site.register(RDError)
admin.site.register(RDIngredient)
admin.site.register(RecipeDesign)
admin.site.register(RMIngredient)
admin.site.register(RecipeInMenu)
admin.site.register(Menu)
