# from django.contrib import admin

# from .models import *

# # Register your models here.

# class RecipeDesignIngredientAdmin(admin.TabularInline):
#     model = RecipeDesignIngredient
#     extra = 1

# class StepsInline(admin.TabularInline):
#     model = Step
#     extra = 1

# class RecipeDesignAdmin(admin.ModelAdmin):
#     # list_display = ("name", "cost_str",)

#     readonly_fields = ['_automatic_errors']
#     filter_horizontal = ("attributes", "diet", "required_accessories")
#     inlines = (RecipeDesignIngredientAdmin, StepsInline)


# # Register your models here.
# admin.site.register(Attribute)
# admin.site.register(Diet)
# admin.site.register(KitchenAccesory)
# admin.site.register(RecipeDesign, RecipeDesignAdmin)

# from django.contrib.auth.models import Permission

# admin.site.register(Permission)