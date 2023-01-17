from django.contrib import admin

from .models import *

# Register your models here.

#
class IngredientInstanceInline(admin.TabularInline):
    model = IngredientInstance
    extra = 1

class StepsInline(admin.TabularInline):
    model = Step
    extra = 1
 

class RecipeAdmin(admin.ModelAdmin):
    list_display = ("name", "thumbnail",) # "get_cost", "get_price", "get_profit",)

    readonly_fields = ['automatic_errors']
    filter_horizontal = ("attributes", "diet", )
    inlines = (IngredientInstanceInline, StepsInline)
    
    

class IngredientAdmin(admin.ModelAdmin):
    list_display = ("name", "price_per_unit", "img",)
    filter_horizontal = ("alergens",)
    
class DeliveryDayAdmin(admin.ModelAdmin):
    filter_horizontal = ("recipes",)

# Register your models here.
admin.site.register(Alergen)
admin.site.register(Attribute)
admin.site.register(Diet)
admin.site.register(KitchenAccesory)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)