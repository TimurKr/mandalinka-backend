from django.contrib import admin
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
# Register your models here.
from home.models import UserProfile, Order
from recepty.models import RecipeOrderInstance

# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'users'
    filter_horizontal = ('food_preferences', 'alergies')
    
# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)

class RecipeOrderInstanceInline(admin.TabularInline):
    model = RecipeOrderInstance
    extra = 2
    

class OrderAdmin(admin.ModelAdmin):
    inlines = (RecipeOrderInstanceInline,)

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Order, OrderAdmin)