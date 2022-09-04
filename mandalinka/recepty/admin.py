from django.contrib import admin

from .models import Recipe, Ingredient, Alergen

# Site customizations
class RecipeAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "description")
    filter_horizontal = ("ingredients",)

class IngredientAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "unit")
    filter_horizontal = ("alergens",)

# class Alergen(admin.ModelAdmin):
#     list_display = ("id", "title")


# Register your models here.
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Alergen)