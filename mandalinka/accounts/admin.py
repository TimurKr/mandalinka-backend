from django.contrib import admin
from accounts.models import *

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    filter_horizontal = ('food_preferences', 'diet', 'alergies', )


admin.site.register(User, UserAdmin)
admin.site.register(Address)
