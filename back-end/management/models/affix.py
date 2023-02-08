from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from django.core.validators import MinValueValidator

from utils.models import TimeStampedMixin, Unit


class AbstractIngredientUse(TimeStampedMixin, models.Model):
    """
    Abstract class offering the basic fields, methods and properties 
    to represent the use of an ingredient in a recipe.

    This class is meant to be inherited by other classes, which will
    define the actual relationship between the ingredient and the recipe.

    Required customizations:
    - ingredient: ForeignKey to an 'Ingredient' model
        - 'Ingredient' model must have a 'unit' property returning a 'Unit' object  
        - 'Ingredient' model must have a 'cost' property returning a float
    - recipe: ForeignKey to a 'Recipe' model

    Optional customizations:
    - alternative_for:
        - default: ForeignKey to 'self'
        - rewrite to None if alternatives are not allowed
    """

    # Override these field to define the relationship between the ingredient and the recipe
    ingredient = None
    recipe = None

    alternative_for = models.ForeignKey('self', related_name="alternatives",
                                        on_delete=models.CASCADE, blank=True, null=True)

    amount = models.FloatField(
        verbose_name=_("Množstvo"), help_text=_("Zadajte množstvo danej potraviny na dve porcie"),
        validators=(MinValueValidator(0),)
    )

    @property
    def unit(self) -> Unit:
        return self.ingredient.unit

    @property
    def cost(self) -> float:
        return self.amount * self.ingredient.cost

    @property
    def cost_str(self) -> str:
        return f'{round(self.cost, 2)} €'

    def __str__(self):
        return f"{self.amount} {self.unit()} {self.ingredient} in {self.recipe}"

    class Meta:
        abstract = True
        unique_together = ('ingredient', 'recipe')


class Attribute(models.Model):
    """
    Model for attributes of recipes, should be selected manually
    """
    name = models.CharField(
        max_length=64,
        unique=True,
    )

    def icon_upload_to(instance, filename):
        return f'custom_icons/attributes/{slugify(instance.__str__())}_icon.{filename.split(".")[1]}'

    icon = models.ImageField(
        upload_to=icon_upload_to,
        help_text=_("Pridajte ikonku"),
        blank=True, null=True
    )

    def __str__(self):
        return self.name


class Alergen(models.Model):
    """Model for representing alergens."""
    name = models.CharField(
        unique=True,
        max_length=64,
    )
    code = models.IntegerField(
        primary_key=True,
        verbose_name=_("Kód")
    )

    def __str__(self):
        return f"{self.code}: {self.name}"


class Diet(models.Model):
    """
    Model for diets of recipes, should be selected manually
    """
    name = models.CharField(
        unique=True,
        max_length=64,
    )

    def icon_upload_to(instance, filename):
        return f'custom_icons/diets/{slugify(instance.__str__())}_icon.{filename.split(".")[1]}'

    icon = models.ImageField(
        upload_to=icon_upload_to,
        help_text=_("Pridajte ikonku"),
        blank=True, null=True
    )

    def __str__(self):
        return self.name


class KitchenAccesory(models.Model):
    """
    Model for kitchen accesories of recipes, should be selected manually
    """
    name = models.CharField(
        unique=True,
        max_length=64,
    )

    def icon_upload_to(instance, filename):
        return f'custom_icons/kitchen_accesories/{slugify(instance.__str__())}_icon.{filename.split(".")[1]}'

    icon = models.ImageField(
        upload_to=icon_upload_to,
        help_text=_("Pridajte ikonku"),
        blank=True, null=True
    )

    def __str__(self):
        return self.name
