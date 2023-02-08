from django.db import models
from django.core.validators import MinValueValidator
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from utils.models import TimeStampedMixin, StatusMixin, Unit
from .affix import Alergen


class IngredientVersion(TimeStampedMixin, StatusMixin, models.Model):
    """
    Model for a single version of an ingredient. Each IngredientVersion has a reference to a Ingredient method.
    This Model represents the part of the Ingredient that can change.
    """

    ingredient = models.ForeignKey('Ingredient', related_name='versions',
                                   verbose_name=_("Ingrediencia"),
                                   on_delete=models.RESTRICT
                                   )

    cost = models.FloatField(
        verbose_name=_("Cena na jednotku"), help_text=_("Zadajte cenu na zvolené množstvo zvolenej jednotky")
    )

    @property
    def cost_str(self) -> str:
        return f'{round(self.cost,2)} €'

    source = models.CharField(
        max_length=64,
        verbose_name=_("Dodávateľ"),
        help_text=_("Toto ešte bude raz foreign key na dodávatela")
    )

    _in_stock_amount = models.FloatField(
        verbose_name=_("Množstvo na sklade"), help_text=_("Automaticky vypočítané poďla IngredientStockChange"),
        editable=False, default=0,
        validators=[MinValueValidator(0)]
    )

    @property
    def in_stock_amount(self) -> float:
        return self._in_stock_amount

    @property
    def in_stock_amount_str(self) -> str:
        return f'{round(self._in_stock_amount,3)} {self.unit}'

    @property
    def is_in_stock(self) -> bool:
        return self._in_stock_amount > 0

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

    def recalculate_in_stock_amount(self):
        self._in_stock_amount = 0
        for stock_change in self.stock_changes:
            self._in_stock_amount += self.unit.from_base(
                stock_change.unit.to_base(stock_change.amount)
            )
        self.save()

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('management:ingredient-detail', kwargs={'pk': self.pk})

    def __str__(self) -> str:
        return f'{self.ingredient} v.{self.version_number}'

    def activate(self) -> None:
        """Activates the IngredientVersion and deactivates all the others"""
        if self.is_active:
            return
        self.ingredient.soft_delete()
        return super().activate()

    def save(self, *args, **kwargs):
        """Saves the IngredientVersion and recalculates the cost"""

        # Validate the ingredient version is editable
        original = self.__class__.objects.filter(pk=self.pk).first()

        if original:
            if self.is_active and original.is_active:
                raise ValueError(
                    _("Can't change the active version of an ingredient. Deactivate or create a new version."))

        else:
            if self.is_active:
                raise ValueError(
                    _("Can't create an active IngredientVersion. Create a new version and activate it."))

        # Validate the unit is the same property as the ingredient unit
        if self.unit.property != self.ingredient.unit.property:
            raise ValueError(
                _("Unit must be of the same property as the ingredient"))

        super().save(*args, **kwargs)


class Ingredient(TimeStampedMixin, models.Model):
    """
    Model for an ingredient. Each IngredientVersion has a reference to a Ingredient method.
    Each Ingredient can only have one IngredientVersion active at a time.
    This Model only represents the part of the Ingredient that does not change.
    """

    name = models.CharField(
        max_length=31,
        unique=True,
        verbose_name=_("Názov"), help_text=_("Názov ingrediencie")
    )

    def img_upload_to(instance, filename):
        return f'ingredients/{slugify(instance.__str__())}.{filename.split(".")[1]}'

    img = models.ImageField(
        upload_to=img_upload_to,
        verbose_name=_("Obrázok"), help_text=_("Pridajte obrazok ku ingrediencií"),
        blank=True, null=True, default=None
    )

    alergens = models.ManyToManyField(Alergen, related_name="ingredients",
                                      blank=True, default=None,
                                      verbose_name=_("Alergény"), help_text=_("Zvolte všetky alergény")
                                      )

    unit = models.ForeignKey(Unit, related_name='uses',
                             on_delete=models.PROTECT
                             )

    @property
    def is_active(self) -> bool:
        return self.active_version is not None

    @property
    def active_version(self) -> IngredientVersion | None:
        """Returns either the active IngredientVersion or False"""
        return self.versions.filter(_status=IngredientVersion.Statuses.ACTIVE).first()

    @property
    def status(self):
        """
        Returns the status of the first that is available in this order:
        1. active IngredientVersion
        2. inactive IngredientVersion
        3. deleted IngredientVersion
        """
        if self.is_active:
            return self.active_version.status
        elif self.versions.filter(_status=IngredientVersion.Statuses.INACTIVE).first():
            return IngredientVersion.Statuses.INACTIVE
        return IngredientVersion.Statuses.DELETED

    @property
    def cost(self):
        """Returns the cost of the active IngredientVersion or None"""
        if self.is_active:
            return self.active_version.cost
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
        if self.is_active:
            self.active_version.deactivate()

    def soft_delete(self):
        """Deletes the active IngredientVersion"""
        if self.is_active:
            self.active_version.soft_delete()


class IngredientStockChange(TimeStampedMixin, models.Model):
    """
    Model representing a change in the stock amount of a paprticular IngredientVersion
    """
    ingredient_version = models.ForeignKey(IngredientVersion, related_name='stock_changes',
                                           on_delete=models.PROTECT
                                           )
    amount = models.FloatField(
        verbose_name=_("Množstvo"), help_text=_("Kladné číslo znamená pridanie, záporné odobranie")
    )
    unit = models.ForeignKey(Unit,
                             on_delete=models.PROTECT, blank=True,
                             verbose_name=_("Jednotka"), help_text=_("Zadajte jednotku")
                             )

    @property
    def amount_str(self) -> str:
        return f'{round(self.in_stock_amount,3)} {self.unit}'

    def _apply(self):
        """
        Applies the change to the IngredientVersion
        Warning: This method does not check if the change has been applied before
        """
        self.ingredient_version._in_stock_amount += self.ingredient_version.unit.from_base(
            self.unit.to_base(self.amount))
        self.ingredient_version.save()

    def _unapply(self):
        """
        Unapplies the change to the IngredientVersion
        WARNING: This method does not check if the change has been applied
        """
        self.ingredient_version._in_stock_amount -= self.ingredient_version.unit.from_base(
            self.unit.to_base(self.amount))
        self.ingredient_version.save()

    def save(self, *args, **kwargs):
        original = IngredientStockChange.objects.filter(pk=self.pk).first()

        if not self.unit:
            self.unit = self.ingredient_version.unit
        elif self.unit.property != self.ingredient_version.unit.property:
            raise ValueError(
                "Unit must be of the same property as the ingredient")

        if original:
            original._unapply()
            self._apply()

        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.ingredient_version}: {self.amount_str}'
