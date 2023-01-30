from django.contrib import admin

from .models import *
from recipes.models import RecipeDeliveryInstance
# Register your models here.

class RecipeDeliveryInstanceInline(admin.TabularInline):
    model = RecipeDeliveryInstance
    fk_name = 'delivery_day'
    extra =1

class DeliveryDayAdmin(admin.ModelAdmin):
    inlines=(RecipeDeliveryInstanceInline, )

admin.site.register(DeliveryDay, DeliveryDayAdmin)