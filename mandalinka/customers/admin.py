from django.contrib import admin

from .models import *

# Register your models here.

class RecipeOrderInstanceInline(admin.TabularInline):
    model = RecipeOrderInstance
    fk_name = 'order'
    extra = 1


class OrderAdmin(admin.ModelAdmin):
    inlines = (RecipeOrderInstanceInline, )
    pass

admin.site.register(Order, OrderAdmin)