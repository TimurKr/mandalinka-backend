from django.contrib import admin

from .models import *

# Register your models here.

#
class IngredientInstanceInline(admin.TabularInline):
    model = IngredientInstance
    extra = 1

class RecipeAdmin(admin.ModelAdmin):
    list_display = ("title", "thumbnail",) # "get_cost", "get_price", "get_profit",)

    filter_horizontal = ("attributes", "diet",)
    inlines = (IngredientInstanceInline,)
    
    

class IngredientAdmin(admin.ModelAdmin):
    list_display = ("title", "price_per_unit", "img",)
    filter_horizontal = ("alergens",)
    
class DeliveryDayAdmin(admin.ModelAdmin):
    filter_horizontal = ("recipes",)

# Register your models here.
admin.site.register(Alergen)
admin.site.register(Attribute)
admin.site.register(Diet)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)