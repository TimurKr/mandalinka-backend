from django.contrib import admin

from .models import *

# Register your models here.

 

class IngredientAdmin(admin.ModelAdmin):
    list_display = ("name", "img",)
    filter_horizontal = ("alergens",)

class IngredientVersionAdmin(admin.ModelAdmin):
    list_display = ("__str__", "parent", "unit", "cost_str",)

class IngredientInRecipeAdmin(admin.ModelAdmin):
    list_display = ("recipe", "ingredient", "amount", "cost_str")
    
class DeliveryDayAdmin(admin.ModelAdmin):
    filter_horizontal = ("recipes",)


class IngredientInRecipeInline(admin.TabularInline):
    model = IngredientInRecipe
    extra = 1

class StepsInline(admin.TabularInline):
    model = Step
    extra = 1

class RecipeAdmin(admin.ModelAdmin):
    list_display = ("name", "cost_str",)

    readonly_fields = ['automatic_errors']
    filter_horizontal = ("attributes", "diet", "required_accessories")
    inlines = (IngredientInRecipeInline, StepsInline)
    

# Register your models here.
admin.site.register(Attribute)
admin.site.register(Diet)
admin.site.register(KitchenAccesory)
admin.site.register(IngredientInRecipe, IngredientInRecipeAdmin)
admin.site.register(Recipe, RecipeAdmin)