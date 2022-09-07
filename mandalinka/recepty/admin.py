from django.contrib import admin

from .models import * 

# Site customizations

# Has to go befor RecipeVersionAdmin
class IngredientInstanceInline(admin.TabularInline):
    model = IngredientInstance
    extra = 1

class RecipeVersionAdmin(admin.ModelAdmin):
    list_display = ("recipe", "version", "avg_rating")
    filter_vertical = ("steps",)
    inlines = (IngredientInstanceInline,)

class RecipeAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "description")

class StepsAdmin(admin.ModelAdmin):
    list_display = ("id", "step")
    filter_horizontal = ("recipes",)


class IngredientAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "unit")
    filter_horizontal = ("alergens",)

class RecipeInstanceAdmin(admin.ModelAdmin):
    pass


# Register your models here.
admin.site.register(RecipeVersion, RecipeVersionAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Step, StepsAdmin)
admin.site.register(IngredientInstance)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Alergen)
admin.site.register(RecipeInstance, RecipeInstanceAdmin)
admin.site.register(Rating)

