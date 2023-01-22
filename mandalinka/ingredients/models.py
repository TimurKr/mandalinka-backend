from django.db import models
from utils.models import TimeStampedMixin, StatusMixin, Unit
from django.utils.text import slugify
from django.core.exceptions import ValidationError

from django.db.models.signals import pre_save
from django.dispatch import receiver

from utils.models import TimeStampedMixin

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
        on_delete=models.PROTECT, default=1
    )

    @property
    def active(self):
        """Returns either the active IngredientVersion or None"""
        return self.versions.filter(_status=IngredientVersion.Statuses.ACTIVE).first() or False

    @property
    def cost(self):
        """Returns the cost of the active IngredientVersion or None"""
        if self.active:
            return self.active.cost
        return None
    
    @property
    def usage_last_month(self):
        """Returns the sum of of times any of its IngredientVersions was used last month"""
        result = 0
        for version in self.versions.all():
            result += 1 # TODO when DeliveryDays are done
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
        on_delete=models.RESTRICT
    )


    "These are only used for forms, to calculate the cost of the ingredient"
    temporary_amount = models.FloatField(
        verbose_name="Množstvo", help_text="Zadajte množstvo"
    )
    temporary_units = models.ForeignKey(Unit, 
        on_delete=models.PROTECT,
        verbose_name="Jednotka", help_text="Zadajte jednotku"
    )

    cost = models.FloatField(
        verbose_name="Cena na jednotku", help_text="Zadajte cenu na zvolenú jednotku"
    )

    source = models.CharField(
        max_length=64, help_text="Toto ešte bude raz foreign key na dodávatela")


    @property
    def cost_str(self):
        return f'{round(self.cost,2)} €'

    @property
    def unit(self) -> Unit:
        return self.parent.unit

    @property
    def version_number(self) -> int:
        return self.parent.versions.filter(date_created__lt=self.date_created).count()
    
    class Meta:
        permissions = [
            ('change_ingredient_status', 'Can change ingredient status'),
        ]
        ordering = ('created',)

    def activate(self):
        """Activates the IngredientVersion and deactivates all the others"""
        if self.active:
            return
        self.parent.deactivate()
        super().activate()

    def __str__(self):
        return f'{self.parent} v.{self.version_number()} - {self.status}'

    def save(self, *args, **kwargs) -> None:
        
        return super().save(*args, **kwargs)


@receiver(pre_save, sender=IngredientVersion)
def validate_editability(sender, instance, **kwargs):
    """Prevents editing of an active IngredientVersion"""
    try:
        old_instance = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        old_instance = None

    if old_instance and old_instance.active and instance.active:
        raise ValueError("Can't change the active version of an ingredient. Deactivate or create a new version.")

@receiver(pre_save, sender=IngredientVersion)
def deactivate_previous_version(sender, instance, **kwargs):
    """If activating a new IngredientVersion, deactivates the previous ones"""
    if instance.active:
        instance.parent.versions.filter(active=True).update(active=False)