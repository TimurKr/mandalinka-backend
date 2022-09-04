from django.contrib import admin

from .models import Recipe, Ingredient, Alergen, IngredientInstance

# Site customizations
class IngredientInstanceInline(admin.TabularInline):
    model = IngredientInstance
    extra = 1

class RecipeAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "description")
    filter_horizontal = ("ingredients",)
    inlines = (IngredientInstanceInline,)

class IngredientAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "unit")
    filter_horizontal = ("alergens",)
    inlines = (IngredientInstanceInline,)


# class Alergen(admin.ModelAdmin):
#     list_display = ("id", "title")


# Register your models here.
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Alergen)
admin.site.register(IngredientInstance)