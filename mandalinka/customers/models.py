from django.db import models

################################# Validators ###################################

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validate_portions(value):
    if value % 2 != 0 or value < 0 or value > 100:
        raise ValidationError(
            _('%(value)s is invalid amount of portions, should be even and on range 0<=x<=100]')
        )

################################### Models #####################################


class RecipeOrderInstance(models.Model):
    recipe = models.ForeignKey('recipes.Recipe', related_name='ratings',
        on_delete=models.PROTECT
    )
    order = models.ForeignKey('customers.Order', related_name='recipes_mid',
        on_delete=models.CASCADE
    )

    portions = models.IntegerField(
        verbose_name='Množstvo porcií', validators=(validate_portions,)
    )

    # Rating
    choices_amount = [
        (None, "Vyhovovala vám porcia"),
        ("1", "Porcia bola malá"),
        ("2", "Porcia mohla byť trochu väčšia"), 
        ("3", "Porcia bola akurát"),
        ("4", "Stačilo by trochu menej"),
        ("5", "Porcia bola príliš veľká")]
    amount_rating = models.CharField(
        blank=True, default=None, null=True, max_length=1,
        choices=choices_amount, 
        verbose_name="Hodnotenie množstva", help_text="Sedelo množstvo jedla s objednanou porciou?"
    )
    
    choices_stars = [
        (None, "Zadajte hodnotenie"),
        ("1", "1"), 
        ("2", "2"), 
        ("3", "3"), 
        ("4", "4"), 
        ("5", "5")]
    taste_rating = models.CharField(
        blank=True, default=None, null=True, max_length=1,
        choices=choices_stars, 
        verbose_name="Chuť", help_text="Viac je lepšie"
    )
    delivery_rating = models.CharField(
        blank=True, default=None, null=True, max_length=1,
        choices=choices_stars, 
        verbose_name="Doručenie", help_text="Viac je lepšie"
    )

    def __str__(self):
        return f"Inštancia objednávky receptu {self.recipe} z {self.order}"


class Order(models.Model):
    user = models.ForeignKey('accounts.User', related_name='orders',
        on_delete=models.PROTECT
    )

    recipes = models.ManyToManyField('recipes.Recipe', through='customers.RecipeOrderInstance', related_name='orders',
        blank=True
    )

    delivery_day = models.ForeignKey('deliveries.DeliveryDay', related_name='orders',
        on_delete=models.PROTECT
    )

    pickup = models.BooleanField(default=False, 
        help_text="True - pickup, False - delivery" 
    )

    def __str__(self):
        return f"Objednávka užívatela {self.user}, dňa {self.delivery_day.date.strftime('%d.%m.%Y')}"

    def toggle_pickup(self):
        if self.pickup: 
            self.pickup = False
        else: 
            self.pickup = True
        self.save()