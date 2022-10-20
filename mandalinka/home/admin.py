from django.contrib import admin
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
# Register your models here.
from home.models import User, Order
from recepty.models import RecipeOrderInstance

# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
class UserInline(admin.StackedInline):
    model = User
    can_delete = False
    verbose_name_plural = 'users'
    filter_horizontal = ('food_preferences', 'alergies')
    

class RecipeOrderInstanceInline(admin.TabularInline):
    model = RecipeOrderInstance
    extra = 2
    

class OrderAdmin(admin.ModelAdmin):
    inlines = (RecipeOrderInstanceInline,)

admin.site.register(User, UserAdmin)
admin.site.register(Order, OrderAdmin)