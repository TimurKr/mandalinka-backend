from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from utils.models import TimeStampedMixin, StatusMixin
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

from management.ingredients.models import Ingredient
from management.affix.models import Attribute, Diet, KitchenAccesory, AbstractIngredientUse


class RDStep(TimeStampedMixin, models.Model):
    """
    Model for steps of recipes
    - number: number of the step
    - text: text of the step
    - thumbnail: image of the step
    - recipe: recipe to which the step belongs
    """

    recipe = models.ForeignKey('RecipeDesign',
                               on_delete=models.CASCADE, related_name="steps"
                               )

    number = models.IntegerField(
        verbose_name=_("Poradie kroku"), validators=(MinValueValidator(1),))

    text = models.TextField(verbose_name="Text")

    def upload_to(instance, filename):
        return f'recipes/{slugify(instance.recipe.__str__())}/steps/{instance.number}.{filename.split(".")[1]}'

    thumbnail = models.ImageField(
        upload_to=upload_to,
        help_text=_("Pridajte thumbnail"),
        blank=True, null=True
    )

    def __str__(self):
        return f'{self.recipe} step n. {self.number}: {self.text}'


class RDError(models.Model):
    """
    Model for errors in recipes.
    - code: code of the error
    - message: error message
    """
    code = models.CharField(max_length=4, unique=True)
    message = models.TextField()

    def __str__(self):
        return f"{self.code}: {self.message}"

    class Meta:
        ordering = ['code']


class RecipeDesign(TimeStampedMixin, StatusMixin, models.Model):
    """
    Model for Recipe Designs. Recipes allow for inheritance, so that a recipe can be
    just a slight change of a previous one. Inheritance can be:
    - exclusive: when the successor is activates, predecessor is deactivated (not vice versa)
    - non-exclusive: when the successor is activated, predecessor is not deactivated
    Both allow for simultaneous activation of multiple inherited recipes,
    but exclusive advises agains it.

    Inherits TimeStampedModel and StatusMixin
    """

    # General

    name = models.CharField(
        max_length=63,
        verbose_name=_("Názov")
    )
    description = models.TextField(
        max_length=127,
        verbose_name=_("Opis jedla"), help_text=_("Zadajte stručný opis jedla")
    )

    def thumbnail_upload_to(instance, filename):
        return f'recipes/{slugify(instance.__str__())}/thumbnail.{filename.split(".")[1]}'
    thumbnail = models.ImageField(
        upload_to=thumbnail_upload_to,
        help_text=_("Pridajte thumbnail"),
        blank=True, null=True
    )

    # Relation to previous

    predecessor = models.ForeignKey('self', related_name='successor',
                                    on_delete=models.PROTECT,
                                    verbose_name=_("Predchodca"),
                                    help_text=_(
                                        "V prípade, že je tento recept iba pozmenený predchádzajúci, zvolte ktorý mu predchádzal"),
                                    blank=True, null=True,
                                    )
    exclusive_inheritance = models.BooleanField(
        default=True,
        verbose_name=_("Deaktivovať predchodcu?"),
        help_text=_('Predchodca bude deaktivovaný až v momente, keď tento recept aktivujete. \
            Toto je vysoko odporúčané, nakoľko hrozia duplicitné recepty v prípade nezaškrtnutia.')
    )

    # Preparation

    difficulty = models.IntegerField(
        choices=[
            (1, _("Easy")),
            (2, _("Medium")),
            (3, _("Hard")),
            (4, _("Profesional")),
        ],
        verbose_name="Náročnosť", help_text="Zadajte náročnosť"
    )
    cooking_time = models.IntegerField(
        validators=(MinValueValidator(2), MaxValueValidator(900)),
        verbose_name=_("Čas varenia"), help_text=_("Zadajte dĺžku varenia od začiatku do hotového jedla v minútach")
    )
    active_cooking_time = models.IntegerField(
        validators=(MinValueValidator(2), MaxValueValidator(300)),
        verbose_name=_("Aktívny čas varenia"), help_text=_("Zadajte čas, ktorý je potrebné venovať sa vareniu")
    )

    attributes = models.ManyToManyField(Attribute, related_name="recipes",
                                        blank=True,
                                        verbose_name=_("Attribúty"), help_text=_("Zadajte všetky atribúty jedla"),
                                        )
    diet = models.ManyToManyField(Diet, related_name='recipes',
                                  blank=True,
                                  verbose_name=("Dieta"), help_text=_("Spadá tento recept do nejakých diet?")
                                  )
    required_accessories = models.ManyToManyField(KitchenAccesory, related_name='recipes',
                                                  blank=True,
                                                  verbose_name=_("Potrebné kuchynské náradie"), help_text=_("Zadajte všetky potrebné kuchynské pomôcky"),
                                                  )

    # Ready to publish checkmarks

    description_finished = models.BooleanField(
        default=False,
        verbose_name=_("Opis finálne hotový"), help_text=_("Odznačte, ak ešte treba opis jedla prerobiť/opraviť/skontrolovať")
    )
    steps_finished = models.BooleanField(
        default=False,
        verbose_name=_("Postup finálne hotový"), help_text=_("Odznačte, ak ešte treba postup prerobiť/opraviť")
    )
    ingredients_finished = models.BooleanField(
        default=False,
        verbose_name=_("Ingrediencie finálne hotové"), help_text=_("Odznačte, ak ešte treba ingrediencie prerobiť/opraviť")
    )

    todo = models.TextField(
        blank=True,
        verbose_name=_("ToDo poznámka"),
        help_text=_(
            "Sem napíš všetko, čo ešte pre tento recept nie je hotové. Veci oddeluj enterom.")
    )

    @property
    def cost(self) -> float:
        cost = 0
        for ingredient in self.ingredients.all():
            cost += ingredient.ingredient.cost
        return cost

    @property
    def cost_str(self) -> str:
        return f'{round(self.cost,2)} €'

    price = models.FloatField(
        verbose_name=_("Predajná cena"),
        default=None, blank=True, null=True
    )

    @property
    def price_str(self) -> str:
        return f'{round(self.price,2)} €'

    @property
    def get_absolute_url(self) -> str:
        return f'/management/recipes/{self.id}/'

    # Errors

    _automatic_errors = models.ManyToManyField(RDError, related_name='recipes',
                                               blank=True,
                                               verbose_name=_("Chyby")
                                               )

    def has_error(self, error: RDError | None = None, code: int | None = None) -> bool:
        """Check if given error or code is valid and
        returns True or False if given error is in this recipe's errors"""
        if not error and not code:
            raise ValueError(_("Either error or code must be provided"))
        if not error:
            try:
                error = RDError.objects.get(code=code)
            except RDError.DoesNotExist:
                raise ValueError(_("Code does not exist"))

        return self._automatic_errors.filter(code=code).exists()

    def add_error(self, error: RDError | None = None, code: int | None = None, save: bool = True) -> None:
        if self.has_error(error, code):
            return
        error = error or RDError.objects.get(code=code)
        self._automatic_errors.add(error)
        if save:
            self.save()

    def remove_error(self, error: RDError | None = None, code: int | None = None, save: bool = True) -> None:
        if not self.has_error(error, code):
            return
        error = error or RDError.objects.get(code=code)
        self._automatic_errors.remove(error)
        if save:
            self.save()

    def _update_auto_errors(self):
        thumbnail_error = RDError.objects.get_or_create(
            code='0', message=_("Chýba thumbnail"))
        steps_error = RDError.objects.get_or_create(
            code='1', message=_("Chýba postup"))
        ingredients_error = RDError.objects.get_or_create(
            code='2', message=_("Chýbajú ingrediencie"))
        attributes_error = RDError.objects.get_or_create(
            code='3', message=_("Chýbajú atribúty"))
        diet_error = RDError.objects.get_or_create(
            code='4', message=_("Chýbajú diety"))
        todo_error = RDError.objects.get_or_create(
            code='5', message=_("Zostáva ToDo list"))

        if not self.thumbnail:
            self.add_error(thumbnail_error)
        else:
            self.remove_error(thumbnail_error)

        if self.steps.count() == 0:
            self.add_error(steps_error)
        else:
            self.remove_error(steps_error)

        if self.ingredients.count() == 0:
            self.add_error(ingredients_error)
        else:
            self.remove_error(ingredients_error)

        if self.attributes.count() == 0:
            self.add_error(attributes_error)
        else:
            self.remove_error(attributes_error)

        if self.diet.count() == 0:
            self.add_error(diet_error)
        else:
            self.remove_error(diet_error)

        if self.todo != "":
            self.add_error(todo_error)
        else:
            self.remove_error(todo_error)

    @property
    def errors_str(self) -> str:
        result = ""

        for error in RDError.objects.all():
            if self.has_error(error):
                result += f'{error.message}, '

        if result:
            result = result[:-2]

        return result

    created_by = models.ForeignKey('accounts.User', related_name="created_recipes",
                                   on_delete=models.PROTECT,
                                   verbose_name=_("Created by"), help_text=_("Zvolte seba"),
                                   )

    @property
    def version(self) -> int:
        version = 0
        predecessor = self.predecessor
        while predecessor:
            version += 1
            predecessor = predecessor.predecessor
        return version or None

    def activate(self):
        if self.exclusive_inheritance and self.predecessor:
            self.predecessor.soft_delete()
        super().activate()

    class Meta:
        permissions = [
            ('change_recipe_status', 'Can change recipe status'),
        ]

        constraints = [
            # Create a check constraint to ensure that cooking_time is greater than
            # or equal to active_cooking_time
            models.CheckConstraint(
                check=models.Q(cooking_time__gte=models.F(
                    'active_cooking_time')),
                name='cooking_time_gte_active_cooking_time',
                violation_error_message=_("Čas varenia musí byť väčší alebo rovný aktívnemu času varenia"))
        ]

        ordering = ['-status_changed', '-created']

    def __str__(self):
        result = self.name
        version = self.version
        if version:
            result += f" v.{str(self.version)}"
        return result

    @property
    def valid_step_numbers(self) -> bool:
        """ Check if all steps have consecutive numbers from 1 up """
        numbers = []

        # Collect all numbers and check uniqueness
        for step in self.steps.all():
            if step.number in numbers:
                return False
            else:
                numbers.append(step.number)

        # Check if all numbers are consecutive from 1 up
        i = 1
        while True:
            if i not in numbers:
                if len(numbers) == i - 1:
                    return True
                else:
                    return False
            i += 1

    def clean(self) -> None:

        # Check if the name is unique, except if it is inherited
        same_name = RecipeDesign.objects.filter(
            name=self.name).exclude(pk=self.pk)

        if same_name.count() != 0:
            fam_tree = []
            recipe = self

            # Collect all predecessors and successors
            while recipe.predecessor:
                fam_tree.append(recipe.predecessor)
            recipe = self
            while recipe.successor:
                fam_tree.append(recipe.successor)

            # Check if the name is used by a recipe that is not a predecessor or successor
            for recipe in same_name:
                if recipe not in fam_tree:
                    raise ValidationError(
                        {'name': _('Meno je už používané receptom, ktorý nieje predchodca ani dedič tohto receptu')})

        # Check if steps are valid
        if not self.valid_step_numbers:
            raise ValidationError(
                {'steps': _('Čísla krokov nie sú korektné')})

        return super().clean()

    def save(self, *args, **kwargs) -> None:
        if self.pk is None:
            super().save(*args, **kwargs)
        self._update_auto_errors()
        return super().save(*args, **kwargs)


class RDIngredient(AbstractIngredientUse):
    """
    Model for 'Ingredient' use in 'RecipeDesign'.
    """

    ingredient = models.ForeignKey(Ingredient, related_name="recipe_designs",
                                   on_delete=models.CASCADE
                                   )
    recipe = models.ForeignKey(RecipeDesign, related_name="ingredients",
                               on_delete=models.CASCADE
                               )
