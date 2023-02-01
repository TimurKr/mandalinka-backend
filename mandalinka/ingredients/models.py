from django.db import models
from utils.models import TimeStampedMixin, StatusMixin, Unit
from django.utils.text import slugify
from django.core.exceptions import ValidationError

from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver


class Alergen(models.Model):
    """Model for representing alergens."""
    name = models.CharField(
        unique=True,
        max_length=63,
        verbose_name="Alergén"
    )
    code = models.IntegerField(
        primary_key=True,
        verbose_name="Kód"
    )

    def __str__(self):
        return f"{self.code}: {self.name}"


class Ingredient(TimeStampedMixin, models.Model):
    """
    Model for a single ingredient. Each IngredientVersion has a reference to a Ingredient method.
    Each Ingredient can only have one IngredientVersion active at a time. 
    This Model only represents the part of the Ingredient that does not change.
    - name - name of the ingredient
    - img - image of the ingredient
    - alergens - alergens that are in the ingredient
    - unit - unit of measurement to use as a default
    """
    name = models.CharField(
        max_length=31,
        unique=True,
        verbose_name="Názov", help_text="Názov ingrediencie"
    )

    def img_upload_to(instance, filename):
        return f'ingredients/{slugify(instance.__str__())}.{filename.split(".")[1]}'

    img = models.ImageField(
        upload_to=img_upload_to,
        verbose_name="Obrázok", help_text="Pridajte obrazok ku ingrediencií",
        blank=True, null=True, default=None
    )

    alergens = models.ManyToManyField(Alergen, related_name="ingredients",
                                      blank=True, default=None,
                                      verbose_name="Alergény", help_text="Zvolte všetky alergény"
                                      )

    unit = models.ForeignKey(Unit, related_name='uses',
                             on_delete=models.PROTECT
                             )

    @property
    def is_active(self) -> bool:
        return self.active is not False

    @property
    def active(self):
        """Returns either the active IngredientVersion or False"""
        return self.versions.filter(_status=IngredientVersion.Statuses.ACTIVE).first() or False

    @property
    def status(self):
        """
        Returns 'active' if there is an active IngredientVersion,
        'inactive' if there is not an active IngredientVersion but a there is an inactive IngredientVersion
        'deleted' if there is not an active IngredientVersion and there is not an inactive IngredientVersion
        """
        if self.active:
            return self.active.status
        elif self.versions.filter(_status=IngredientVersion.Statuses.INACTIVE).first():
            return IngredientVersion.Statuses.INACTIVE
        return IngredientVersion.Statuses.DELETED

    @property
    def cost(self):
        """Returns the cost of the active IngredientVersion or None"""
        active = self.active
        if active:
            return active.cost
        return None

    @property
    def usage_last_month(self) -> int:
        """Returns the sum of of times any of its IngredientVersions was used last month"""
        result = 0
        for version in self.versions.all():
            result += 1  # TODO when DeliveryDays are done
        return result

    def __str__(self):
        return self.name

    def deactivate(self):
        """Deactivates the active IngredientVersion"""
        if self.active:
            self.active.deactivate()


class IngredientVersion(TimeStampedMixin, StatusMixin, models.Model):
    """
    Model for a single version of an ingredient. Each IngredientVersion has a reference to a Ingredient method.
    This Model represents the part of the Ingredient that can change. 
    """

    ingredient = models.ForeignKey(Ingredient, related_name='versions',
                                   verbose_name="Ingrediencia",
                                   on_delete=models.RESTRICT
                                   )

    cost = models.FloatField(
        verbose_name="Cena na jednotku", help_text="Zadajte cenu na zvolené množstvo zvolenej jednotky"
    )

    @property
    def cost_str(self) -> str:
        return f'{round(self.cost,2)} €'

    source = models.CharField(
        max_length=64,
        verbose_name="Dodávateľ",
        help_text="Toto ešte bude raz foreign key na dodávatela"
    )

    _in_stock_amount = models.FloatField(
        verbose_name="Množstvo na sklade", help_text="Množstvo na sklade môže byť špecifikované iba výrobou objektu IngredientStockChange",
        editable=False, default=0
    )

    @property
    def in_stock(self) -> float:
        return self._in_stock_amount

    @property
    def in_stock_str(self) -> str:
        return f'{round(self._in_stock_amount,3)} {self.unit}'

    @property
    def unit(self) -> Unit:
        return self.ingredient.unit

    @property
    def version_number(self) -> int:
        return self.ingredient.versions.filter(created__lt=self.created).count()

    class Meta:
        permissions = [
            ('change_ingredient_status', 'Can change ingredient status'),
        ]
        ordering = ('created',)

    def activate(self):
        """Activates the IngredientVersion and deactivates all the others"""
        if self.active:
            return
        self.ingredient.deactivate()
        super().activate()

    def recalculate_in_stock_amount(self):
        self._in_stock_amount = 0
        for stock_change in self.stock_changes:
            self._in_stock_amount += self.unit.from_base(
                stock_change.unit.to_base(stock_change.amount)
            )
        self.save()

    def __str__(self) -> str:
        return f'{self.ingredient} v.{self.version_number}'

    def save(self, *args, **kwargs):
        """Saves the IngredientVersion and recalculates the cost"""

        # Validate the ingredient version is editable
        original = self.__class__.objects.filter(pk=self.pk).first()
        if original and original.active and self.active:
            raise ValueError(
                "Can't change the active version of an ingredient. Deactivate or create a new version.")

        # Validate the unit is the same property as the ingredient unit
        if self.unit.property != self.ingredient.unit.property:
            raise ValueError(
                "Unit must be of the same property as the ingredient")

        # If creating and already active, raise an error
        if not original and self.active:
            raise ValueError(
                "Can't create an active IngredientVersion. Create a new version and activate it.")

        # If activating, deactivate the previous versions
        if self.active and not original.active:
            for version in self.ingredient.versions.all():
                version.soft_delete()

        super().save(*args, **kwargs)


class IngredientStockChange(TimeStampedMixin, models.Model):
    """
    Model for changing the _in_stock_amount of an IngredientVersion.
    Recalculates the _in_stock_amount of the IngredientVersion when saved.
    """
    ingredient_version = models.ForeignKey(IngredientVersion, related_name='stock_changes',
                                           on_delete=models.PROTECT
                                           )
    amount = models.FloatField(
        verbose_name="Množstvo", help_text="Kladné číslo znamená pridanie, záporné odobranie"
    )
    unit = models.ForeignKey(Unit,
                             on_delete=models.PROTECT, blank=True,
                             verbose_name="Jednotka", help_text="Zadajte jednotku"
                             )

    @property
    def amount_str(self) -> str:
        return f'{round(self.in_stock_amount,2)} {self.unit}'

    def _apply(self):
        self.ingredient_version._in_stock_amount += self.ingredient_version.unit.from_base(
            self.unit.to_base(self.amount))
        self.ingredient_version.save()

    def _unapply(self):
        self.ingredient_version._in_stock_amount -= self.ingredient_version.unit.from_base(
            self.unit.to_base(self.amount))
        self.ingredient_version.save()

    def save(self, *args, **kwargs):
        original = self.__class__.objects.filter(pk=self.pk).first()

        if original:
            original._unapply()
            self._apply()

        if not self.unit:
            self.unit = self.ingredient_version.unit
        elif self.unit.property != self.ingredient_version.unit.property:
            raise ValueError(
                "Unit must be of the same property as the ingredient")

        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.ingredient_version}: {self.amount_str}'
