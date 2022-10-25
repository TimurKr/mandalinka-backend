from django.contrib import admin
from accounts.models import *

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    filter_horizontal = ('food_preferences', 'alergies', 'diet',)



admin.site.register(User, UserAdmin)
