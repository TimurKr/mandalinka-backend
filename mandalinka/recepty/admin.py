from django.contrib import admin

from .models import Recipe, Ingredient, Alergen, IngredientInstance, Step, RecipeVersion

# Site customizations
# Has to go befor RecipeVersionAdmin
class IngredientInstanceInline(admin.TabularInline):
    model = IngredientInstance
    extra = 1

class RecipeVersionAdmin(admin.ModelAdmin):
    list_display = ("id", "recipe")
    filter_horizontal = ("steps", "ingredients")
    inlines = (IngredientInstanceInline,)

class RecipeAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "description")

class StepsAdmin(admin.ModelAdmin):
    list_display = ("id", "step")
    filter_horizontal = ("recipes",)


class IngredientAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "unit")
    filter_horizontal = ("alergens",)


# class Alergen(admin.ModelAdmin):
#     list_display = ("id", "title")


# Register your models here.
admin.site.register(RecipeVersion, RecipeVersionAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Step, StepsAdmin)
admin.site.register(IngredientInstance)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Alergen)

