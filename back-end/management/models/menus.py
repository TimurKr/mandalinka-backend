from django.db import models
from django.utils.translation import gettext_lazy as _

from utils.models import TimeStampedMixin
from .affix import AbstractIngredientUse
from .ingredients import IngredientVersion
from .recipe_designs import RecipeDesign


class Menu(TimeStampedMixin, models.Model):
    date = models.DateField(verbose_name=_('Dátum'),
                            blank=False, unique=True
                            )

    _public = models.BooleanField(default=False,
                                  help_text=_(
                                      'Označuje, či je recept verejný.'),
                                  editable=False,
                                  )

    @property
    def public(self) -> bool:
        return self._public

    def __str__(self):
        return f"Menu na deň {self.date.strftime('%d.%m.%Y')}"

    def _generate_orders(self) -> None:
        """"
        Generate an order for all active users
        If the order has been created and the user is subscribed, automaticaly order best recipes
        """
        # from django.apps import apps
        # User = apps.get_model('accounts', 'User')

        # for user in User.objects.filter(is_active=True):
        #     (order, created) = user.orders.get_or_create(delivery_day=self)
        #     if created and user.is_subscribed:
        #         order.automaticaly_generate()
        pass

    def save(self, *args, **kwargs):
        """
        Saves the object and generates all future orders for all users

        public: bool -> True makes public true and generates orders for all users
        """
        original = Menu.objects.filter(pk=self.pk).first()

        if original and not original.public and self.public:
            self._generate_orders()

        else:
            super().save(*args, **kwargs)


class RecipeInMenu(TimeStampedMixin, models.Model):
    recipe_design = models.ForeignKey(RecipeDesign, related_name="menus",
                                      on_delete=models.PROTECT
                                      )
    menu = models.ForeignKey(Menu, related_name='recipes',
                             on_delete=models.PROTECT
                             )

    cost = models.FloatField(
        verbose_name='Reálne náklady',
        blank=True, null=True, default=None,
    )
    price = models.FloatField(
        verbose_name='Predajná cena',
        blank=True, null=True, default=None,
    )

    class Meta:
        unique_together = ('recipe_design', 'menu')


class RMIngredient(AbstractIngredientUse):
    """
    Model for 'IngredientVersion' use in 'RecipeInMenu'.
    """

    ingredient = models.ForeignKey(IngredientVersion, related_name="recipe_designs",
                                   on_delete=models.CASCADE
                                   )
    recipe = models.ForeignKey(RecipeInMenu, related_name="ingredients",
                               on_delete=models.CASCADE
                               )
