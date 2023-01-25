from django.contrib import admin

from .models import *
from recipes.models import RecipeDeliveryInstance
# Register your models here.

class RecipeDeliveryInstanceInline(admin.TabularInline):
    model = RecipeDeliveryInstance
    extra =1

class DeliveryDayAdmin(admin.ModelAdmin):
    filter_horizontal = ('recipes', )
    inlines=(RecipeDeliveryInstanceInline, )

admin.site.register(DeliveryDay, DeliveryDayAdmin)