from django.contrib import admin

# Register your models here.
from home.models import User, Order, Address, Diet
from recepty.models import RecipeOrderInstance
    

class UserAdmin(admin.ModelAdmin):
    # inlines = ('addresses',)
    pass

class RecipeOrderInstanceInline(admin.TabularInline):
    model = RecipeOrderInstance
    extra = 2
    

class OrderAdmin(admin.ModelAdmin):
    inlines = (RecipeOrderInstanceInline,)

# Re-register UserAdmin
admin.site.register(User, UserAdmin)
admin.site.register(Address)
admin.site.register(Diet)
admin.site.register(Order, OrderAdmin)