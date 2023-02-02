from django.contrib import admin

# Register your models here.

from .models.affix import Attribute, Alergen, Diet, KitchenAccesory
from .models.ingredients import Ingredient, IngredientVersion, IngredientStockChange
from .models.recipe_designs import RDStep, RDError, RDIngredient, RecipeDesign
from .models.menus import RMIngredient, RecipeInMenu, Menu

admin.site.register(Attribute)
admin.site.register(Alergen)
admin.site.register(Diet)
admin.site.register(KitchenAccesory)
admin.site.register(Ingredient)
admin.site.register(IngredientVersion)
admin.site.register(IngredientStockChange)
admin.site.register(RDStep)
admin.site.register(RDError)
admin.site.register(RDIngredient)
admin.site.register(RecipeDesign)
admin.site.register(RMIngredient)
admin.site.register(RecipeInMenu)
admin.site.register(Menu)
