from django.contrib import admin

from .models import Recipe, Ingredient

# Site customizations
class RecipeAdmin(admin.ModelAdmin):
    list_display = ("id", "title")
    filter_horizontal = ("ingredients",)


# Register your models here.
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient)