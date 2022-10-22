from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Register your models here.
from home.models import User, Order
from recepty.models import RecipeOrderInstance
    

class RecipeOrderInstanceInline(admin.TabularInline):
    model = RecipeOrderInstance
    extra = 2
    

class OrderAdmin(admin.ModelAdmin):
    inlines = (RecipeOrderInstanceInline,)

# Re-register UserAdmin
admin.site.register(User)
admin.site.register(Order, OrderAdmin)