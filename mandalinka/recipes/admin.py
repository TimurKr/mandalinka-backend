from django.contrib import admin

from .models import *

# Register your models here.

 

class IngredientAdmin(admin.ModelAdmin):
    list_display = ("name", "img",)
    filter_horizontal = ("alergens",)

class IngredientVersionAdmin(admin.ModelAdmin):
    list_display = ("__str__", "parent", "unit", "print_cost",)

class IngredientInRecipeAdmin(admin.ModelAdmin):
    list_display = ("recipe", "ingredient", "amount", "print_cost")
    
class DeliveryDayAdmin(admin.ModelAdmin):
    filter_horizontal = ("recipes",)


class IngredientInRecipeInline(admin.TabularInline):
    model = IngredientInRecipe
    extra = 1

class StepsInline(admin.TabularInline):
    model = Step
    extra = 1

class RecipeAdmin(admin.ModelAdmin):
    list_display = ("name", "print_cost",) # "get_cost", "get_price", "get_profit",)

    readonly_fields = ['automatic_errors']
    filter_horizontal = ("attributes", "diet", "required_accessories")
    inlines = (IngredientInRecipeInline, StepsInline)
    

# Register your models here.
admin.site.register(Alergen)
admin.site.register(Attribute)
admin.site.register(Diet)
admin.site.register(Unit)
admin.site.register(KitchenAccesory)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(IngredientVersion, IngredientVersionAdmin)
admin.site.register(IngredientInRecipe, IngredientInRecipeAdmin)
admin.site.register(Recipe, RecipeAdmin)