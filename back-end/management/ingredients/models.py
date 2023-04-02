import datetime
from django.db import models
from django.core.validators import MinValueValidator
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save, pre_delete, post_delete
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from utils.models import TimeStampedMixin, StatusMixin, Unit
from management.affix.models import Alergen


class IngredientVersion(TimeStampedMixin, StatusMixin, models.Model):
    """
    Model for a single version of an ingredient. Each IngredientVersion has a reference to a Ingredient method.
    This Model represents the part of the Ingredient that can change.
    """

    ingredient = models.ForeignKey('Ingredient', related_name='versions',
                                   verbose_name=_("Ingrediencia"),
                                   on_delete=models.RESTRICT
                                   )

    _cost = models.FloatField(
        verbose_name=_("Cena na jednotku"),
        help_text=_("Zadajte cenu na zvolené množstvo zvolenej jednotky"),
        validators=[MinValueValidator(0, message=_("Cena musí byť kladná"))],
        null=True, blank=True
    )

    @property
    def cost(self) -> float:
        return self._cost

    @property
    def cost_str(self) -> str:
        return f'{round(self.cost,2)} €'

    def update_cost(self) -> None:
        new_cost = None
        last_order = self.orders.order_by('-order_date').first()
        if last_order:
            new_cost = last_order.cost / \
                self.unit.from_base(last_order.unit.to_base(last_order.amount))

        if new_cost != self._cost:
            self._cost = new_cost
            self.save()

    source = models.CharField(
        max_length=64,
        verbose_name=_("Dodávateľ"),
        help_text=_("Toto ešte bude raz foreign key na dodávatela")
    )

    _in_stock_amount = models.FloatField(
        verbose_name=_("Množstvo na sklade"), help_text=_("Automaticky vypočítané poďla IngredientStockChange"),
        editable=False, default=0,
        validators=[MinValueValidator(
            0, message=_("Množstvo musí byť kladné"))]
    )

    def update_in_stock_amount(self) -> None:
        in_stock_amount = 0
        for order in self.orders.filter(_in_stock_amount__gt=0):
            in_stock_amount += self.unit.from_base(
                order.unit.to_base(order.in_stock_amount))

        if in_stock_amount != self._in_stock_amount:
            self._in_stock_amount = in_stock_amount
            self.save()

    @property
    def in_stock_amount(self) -> float:
        return self._in_stock_amount

    @property
    def in_stock_amount_str(self) -> str:
        return f'{round(self._in_stock_amount,3)} {self.unit}'

    expiration_period = models.IntegerField(
        verbose_name=_("Expiračný čas"), help_text=_("Zadajte množstvo dní"),
        default=7, validators=[MinValueValidator(1)]
    )

    @property
    def orders(self) -> models.QuerySet:
        return IngredientVersionStockOrder.objects.filter(ingredient_version=self)

    @property
    def removals(self) -> models.QuerySet:
        return IngredientVersionStockRemove.objects.filter(ingredient_version=self)

    @property
    def is_in_stock(self) -> bool:
        return self._in_stock_amount > 0

    @property
    def unit(self) -> Unit:
        return self.ingredient.unit

    @property
    def version_number(self) -> int:
        return self.ingredient.versions.filter(created__lt=self.created).count() + 1

    class Meta:
        permissions = [
            ('change_ingredient_status', 'Can change ingredient status'),
        ]
        ordering = ('created',)

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

        if not original and self.is_active:
            raise ValidationError(
                _("Nemôžete vytvoriť aktívnu verziu ingrediencie."))

        return super().save(*args, **kwargs)


@receiver(post_save, sender=IngredientVersion)
def update(sender: IngredientVersion, instance: IngredientVersion, **kwargs):
    instance.update_in_stock_amount()
    instance.update_cost()


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
        # TODO when DeliveryDays are done
        # for version in self.versions.all():
        #     result += 1
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
        validators=[MinValueValidator(0.000000001)],
    )
    unit = models.ForeignKey(
        Unit,
        on_delete=models.PROTECT,
        verbose_name=_("Jednotka"), help_text=_("Zadajte jednotku")
    )

    @property
    def amount_str(self) -> str:
        return f'{round(self.amount,3)} {self.unit}'

    def save(self, *args, **kwargs):
        """
        Checks if unit is the same property as the IngredientVersion's unit. 

        Override this method and call it at the and to implement applying the change to the IngredientVersion
        """

        if not self.unit:
            self.unit = self.ingredient_version.unit
        elif self.unit.property != self.ingredient_version.unit.property:
            raise ValidationError(
                "Unit must be of the same property as the ingredient")

        return super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.ingredient_version}: {self.amount_str}'

    class Meta:
        ordering = ('created',)


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

    date = models.DateTimeField(
        default=datetime.datetime.now,
        verbose_name=_("Dátum"),
        help_text=_("Zadajte dátum odobratia")
    )

    def _apply(self):
        orders = self.ingredient_version.orders.filter(
            _in_stock_amount__gt=0).order_by('delivery_date')

        self_amount = self.unit.to_base(self.amount)

        for order in orders:
            order_in_stock = order.unit.to_base(order.in_stock_amount)
            if order_in_stock >= self_amount:
                order._in_stock_amount -= order.unit.from_base(self_amount)
                order.save()
                break
            else:
                self_amount -= order_in_stock
                order._in_stock_amount = 0
                order.save()

    def _unapply(self):
        orders = self.ingredient_version.orders.filter(
            is_delivered=True).order_by('-delivery_date')
        self_amount = self.unit.to_base(self.amount)
        for order in orders:
            order_missing = order.unit.to_base(
                order.amount - order.in_stock_amount)
            if order_missing >= self_amount:
                order._in_stock_amount += order.unit.from_base(self_amount)
                order.save()
                break
            else:
                self_amount -= order_missing
                order._in_stock_amount = order.amount
                order.save()

    class Meta:
        ordering = ('created',)


@receiver(pre_save, sender=IngredientVersionStockRemove)
def apply_remove(sender, instance: IngredientVersionStockRemove, **kwargs):
    original = sender.objects.filter(pk=instance.pk).first()
    if original:
        og_amount = original.unit.to_base(original.amount)
        new_amount = instance.unit.to_base(instance.amount)
        if og_amount != new_amount:
            original._unapply()
            instance._apply()
    else:
        instance._apply()


@receiver(pre_delete, sender=IngredientVersionStockRemove)
def unapply_remove(sender, instance: IngredientVersionStockRemove, **kwargs):
    instance._unapply()


class IngredientVersionStockOrder(IngredientVersionStockChange):

    parent = models.OneToOneField(IngredientVersionStockChange, parent_link=True,
                                  on_delete=models.PROTECT, primary_key=True, related_name='ordered')

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

    expiration_date = models.DateField(
        verbose_name=_("Dátum expirácie"),
        help_text=_("Zadajte dátum a čas expirácie")
    )

    is_expired = models.BooleanField(
        default=False,
        verbose_name=_("Expirované"),
        help_text=_("Zaškrtnite, ak expirovalo")
    )

    cost = models.FloatField(
        verbose_name=_("Cena"),
        validators=[MinValueValidator(0)],
        help_text=_("Zadajte cenu")
    )

    _in_stock_amount = models.FloatField(
        verbose_name=_("Množstvo v sklade"),
        validators=[MinValueValidator(0)],
        help_text=_("Zadajte množstvo na sklade"),
        default=0
    )

    @property
    def in_stock_amount(self) -> float:
        return self._in_stock_amount

    class Meta:
        ordering = ('-order_date', 'delivery_date', 'created')

    def save(self, *args, **kwargs):
        if self.pk:
            original = IngredientVersionStockOrder.objects.get(pk=self.pk)

            if self.is_delivered and not original.is_delivered:
                self._in_stock_amount = self.amount
            elif not self.is_delivered and original.is_delivered:
                self._in_stock_amount = 0

            if self.is_expired and not original.is_expired:
                IngredientVersionStockRemove.objects.create(
                    ingredient_version=self.ingredient_version,
                    amount=self.in_stock_amount,
                    unit=self.unit,
                    reason="expired",
                    date=self.expiration_date
                )
                return
            if self.in_stock_amount > 0:
                self.is_expired = False
            if self.is_expired:
                self._in_stock_amount = 0
        else:
            if self.is_delivered:
                self._in_stock_amount = self.amount
            else:
                self._in_stock_amount = 0

        if self.is_delivered and self.in_stock_amount == 0:
            self.is_expired = True

        return super().save(*args, **kwargs)


@receiver(post_save, sender=IngredientVersionStockOrder)
def update_in_stock_amount(sender, instance: IngredientVersionStockOrder, **kwargs):
    instance.ingredient_version.update_in_stock_amount()


@receiver(post_save, sender=IngredientVersionStockOrder)
def update_cost(sender, instance: IngredientVersionStockOrder, **kwargs):
    instance.ingredient_version.update_cost()


@receiver(pre_delete, sender=IngredientVersionStockOrder)
def unapply_order(sender, instance, **kwargs):
    if instance.is_delivered:
        raise ValidationError(
            f"Doručená objednávka č.{instance.id} nemôže byť zmazaná."
        )


@receiver(post_delete, sender=IngredientVersionStockOrder)
def update_cost(sender, instance: IngredientVersionStockOrder, **kwargs):
    instance.ingredient_version.update_cost()
