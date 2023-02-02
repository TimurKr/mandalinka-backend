from django.db import models
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from utils.validators import validate_positivity

from management.models.ingredients import Ingredient, IngredientVersion
from utils.models import StatusMixin, Unit, TimeStampedMixin

from django.db.models.signals import post_save
from django.dispatch import receiver
################################# Validators ###################################


def validate_cooking_time_range(value):
    if value >= 300 or value < 1:
        raise ValidationError(
            _('%(value)s is not in the required cooking range [1, 300]'),
            params={'value': value},
        )

################################# Models ###################################


# class RecipeDeliveryInstance(models.Model):
#     recipe_design = models.ForeignKey(RecipeDesign, related_name="delivery_days",
#                                       on_delete=models.PROTECT
#                                       )
#     delivery_day = models.ForeignKey('deliveries.DeliveryDay', related_name='recipes',
#                                      on_delete=models.PROTECT
#                                      )

#     cost = models.FloatField(
#         verbose_name='Reálne náklady',
#         blank=True, null=True, default=None,
#     )
#     price = models.FloatField(
#         verbose_name='Predajná cena',
#         blank=True, null=True, default=None,
#     )

#     class Meta:
#         unique_together = ('recipe_design', 'delivery_day')
