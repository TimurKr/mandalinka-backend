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
    def orders(self) -> models.QuerySet:
        return IngredientVersionStockOrder.objects.filter(ingredient_version=self)

    @property
    def removes(self) -> models.QuerySet:
        return IngredientVersionStockRemove.objects.filter(ingredient_version=self)

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

    @property
    def get_absolute_url(self) -> str:
        return f'/management/ingredients/{self.ingredient.id}/{self.id}'

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

    extra_info = models.TextField(
        verbose_name=_("Extra informácie"), help_text=_("Extra informácie o ingrediencii"),
        blank=True, null=True, default=None
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
        """True if there is at least one active ingredient"""
        return self.active_version is not None

    @property
    def is_inactive(self) -> bool:
        """True if there is not an active ingredient, but there is at least one inactive ingredient"""
        return not self.is_active and self.versions.get_inactive().first() is not None

    @property
    def is_deleted(self) -> bool:
        """True if there is no active ingredient, no inactive ingredient and at least one deleted ingredient"""
        return not self.is_active and not self.is_inactive and self.versions.get_deleted().first() is not None

    @property
    def active_version(self) -> IngredientVersion | None:
        """Returns either the active IngredientVersion or False"""
        return self.versions.get_active().first()

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
    def cost(self) -> float | None:
        """Returns the cost of the active IngredientVersion or None"""
        if self.is_active:
            return self.active_version.cost
        return None

    @property
    def cost_str(self) -> str | None:
        """Returns the cost of the active IngredientVersion or None"""
        if self.is_active:
            return self.active_version.cost_str
        return None

    @property
    def in_stock_amount(self) -> float | None:
        """Returns the sum of in_stock_amount of all IngredientVersions"""
        sum = 0
        for version in self.versions.all():
            sum += version.in_stock_amount
        return sum

    @property
    def usage_last_month(self) -> int:
        """Returns the sum of of times any of its IngredientVersions was used last month"""
        result = 0
        for version in self.versions.all():
            result += 1  # TODO when DeliveryDays are done
        return result

    @property
    def get_absolute_url(self) -> str:
        return f'/management/ingredients/{self.pk}/'

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


class IngredientVersionStockChange(TimeStampedMixin, models.Model):
    """
    Model representing a change in the stock amount of a paprticular IngredientVersion.
    Should not be used by itself, always use children models.
    Available children models:
    - IngredientVersionStockRemove
    - IngredientVersionStockOrder
    - TODO: Order itself
    """
    ingredient_version = models.ForeignKey(IngredientVersion, related_name='stock_changes',
                                           on_delete=models.PROTECT
                                           )
    amount = models.FloatField(
        verbose_name=_("Množstvo"),
        validators=[MinValueValidator(0)],
    )
    unit = models.ForeignKey(Unit,
                             on_delete=models.PROTECT, blank=True,
                             verbose_name=_("Jednotka"), help_text=_("Zadajte jednotku")
                             )

    @property
    def amount_str(self) -> str:
        return f'{round(self.in_stock_amount,3)} {self.unit}'

    def _add(self):
        """
        Applies the change to the IngredientVersion
        Warning: This method does not check if the change has been applied before
        """
        self.ingredient_version._in_stock_amount += self.ingredient_version.unit.from_base(
            self.unit.to_base(self.amount))
        self.ingredient_version.save()

    def _remove(self):
        """
        Unapplies the change to the IngredientVersion
        WARNING: This method does not check if the change has been applied
        """
        self.ingredient_version._in_stock_amount -= self.ingredient_version.unit.from_base(
            self.unit.to_base(self.amount))
        self.ingredient_version.save()

    def save(self, *args, **kwargs):
        """
        Checks if unit is the same property as the IngredientVersion's unit. 

        Override this method and call it at the and to implement applying the change to the IngredientVersion
        """

        if not self.unit:
            self.unit = self.ingredient_version.unit
        elif self.unit.property != self.ingredient_version.unit.property:
            raise ValueError(
                "Unit must be of the same property as the ingredient")

        return super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.ingredient_version}: {self.amount_str}'


class IngredientVersionStockRemove(IngredientVersionStockChange):

    parent = models.OneToOneField(IngredientVersionStockChange, parent_link=True,
                                  on_delete=models.PROTECT, primary_key=True, related_name='removed')

    class Reason:
        EXPIRED = 'expired'
        WENT_BAD = 'went_bad'
        OTHER = 'other'     # Change meta constraints if you change this
        CHOICES = (
            (EXPIRED, _('Vypršal termín spotreby')),
            (WENT_BAD, _('Pokazilo sa')),
            (OTHER, _('Iný dôvod')),
        )

    reason = models.CharField(
        max_length=20,
        choices=Reason.CHOICES,
        default=Reason.OTHER,
        verbose_name=_("Dôvod"),
        help_text=_("Zvolte dôvod odobratia")
    )

    description = models.TextField(
        blank=True, null=True, default=None,
        verbose_name=_("Popis"),
        help_text=_("Zadajte popis odobratia")
    )

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(reason__exact='other') & models.Q(
                    description__isnull=True),
                name='%(app_label)s_%(class)s_other_reason_has_no_description'
            )
        ]

    def save(self, *args, **kwargs):
        """Applies the change to the IngredientVersion always when being saved"""
        original = IngredientVersionStockRemove.objects.filter(
            pk=self.pk).first()

        if original:
            original._add()

        self._remove()
        return super().save(*args, **kwargs)


class IngredientVersionStockOrder(IngredientVersionStockChange):

    parent = models.OneToOneField(IngredientVersionStockChange, parent_link=True,
                                  on_delete=models.CASCADE, primary_key=True, related_name='extension')

    description = models.TextField(
        blank=True, null=True, default=None,
        verbose_name=_("Popis"),
        help_text=_("Zadajte popis pridania")
    )

    order_date = models.DateTimeField(
        verbose_name=_("Dátum objednávky"),
        help_text=_("Zadajte dátum a čas objednávky")
    )

    delivery_date = models.DateTimeField(
        verbose_name=_("Dátum dodania"),
        help_text=_("Zadajte dátum a čas dodania")
    )

    is_delivered = models.BooleanField(
        default=False,
        verbose_name=_("Bolo dodané"),
        help_text=_("Zaškrtnite, ak bolo dodané")
    )

    def save(self, *args, **kwargs):
        original = IngredientVersionStockOrder.objects.filter(
            pk=self.pk).first()

        if original:
            if not original.is_delivered and self.is_delivered:
                self._add()
            elif original.is_delivered and not self.is_delivered:
                self._remove()
