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
    filter_horizontal = ("attributes",)
    
class StepsAdmin(admin.ModelAdmin):
    filter_horizontal = ("recipes",)
    
class IngredientAdmin(admin.ModelAdmin):
    filter_horizontal = ("alergens",)
    
class DeliveryDayAdmin(admin.ModelAdmin):
    filter_horizontal = ("recipes",)

# Register your models here.
admin.site.register(RecipeVersion, RecipeVersionAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Step, StepsAdmin)
admin.site.register(IngredientInstance)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Alergen)
admin.site.register(FoodAttribute)
admin.site.register(DeliveryDay, DeliveryDayAdmin)

