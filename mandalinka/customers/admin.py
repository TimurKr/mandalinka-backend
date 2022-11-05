from django.contrib import admin

from .models import *

# Register your models here.

class RecipeOrderInstanceInline(admin.TabularInline):
    model = RecipeOrderInstance
    extra = 1


class OrderAdmin(admin.ModelAdmin):
    inlines = (RecipeOrderInstanceInline, )

admin.site.register(Order, OrderAdmin)