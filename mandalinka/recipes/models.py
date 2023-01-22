from django.db import models
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from utils.validators import validate_positivity

from ingredients.models import Ingredient, IngredientVersion
from utils.models import StatusMixin, Unit, TimeStampedMixin
################################# Validators ###################################

def validate_cooking_time_range(value):
    if value >= 300 or value < 1:
        raise ValidationError(
            _('%(value)s is not in the required cooking range [1, 300]'),
            params = {'value': value},
        )

################################# Models ###################################

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
        help_text="Pridajte ikonku", 
        blank=True, null=True
    )

    def __str__(self):
        return self.name

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
        help_text="Pridajte ikonku", 
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
        help_text="Pridajte ikonku", 
        blank=True, null=True
    )

    def __str__(self):
        return self.name


class IngredientInRecipe(models.Model):
    """
    Many to many relationship between recipes and ingredients.
    The relationship is to Ingredient, rather than IngredientVersion, because
    versions may go obsolete, but the relationship should remain. 
    When a delivery containg a given recipe is finalized, a copy of this is 
    created in an archive but with the exact IngredientVersion used on that day.
    """
    ingredient = models.ForeignKey(IngredientVersion, related_name="recipes_mid", 
        on_delete=models.CASCADE
    )
    recipe = models.ForeignKey('recipes.Recipe', related_name="ingredients_mid",
        on_delete=models.CASCADE
    )

    amount = models.FloatField(
        verbose_name="Množstvo", help_text="Zadajte množstvo danej potraviny na dve porcie",
        validators=(validate_positivity,)
    )

    @property
    def unit(self):
        return self.ingredient.unit

    @property
    def cost(self):
        return self.amount * self.ingredient.cost

    @property
    def cost_str(self):
        return f'{round(self.cost(), 2)} €'
    
    def __str__(self):
        return f"{self.amount} {self.unit()} {self.ingredient} in {self.recipe}"


class Step(TimeStampedMixin, models.Model):
    """
    Model for steps of recipes
    - number: number of the step
    - text: text of the step
    - thumbnail: image of the step
    - recipe: recipe to which the step belongs
    """

    number = models.IntegerField(verbose_name="Poradie kroku", validators=[validate_positivity])
    text = models.TextField(verbose_name="Text")

    def upload_to(instance, filename):
        return f'recipes/{slugify(instance.recipe.__str__())}/steps/{instance.number}.{filename.split(".")[1]}'

    thumbnail = models.ImageField(
        upload_to=upload_to, 
        help_text="Pridajte thumbnail", 
        blank=True, null=True
    )

    recipe = models.ForeignKey('Recipe', 
        on_delete=models.CASCADE, related_name="steps"
    )

    def __str__(self):
        return f'{self.recipe} step n. {self.number}: {self.text}'

class RecipeError(models.Model):
    """
    Model for errors in recipes.
    - code: code of the error
    - message: error message
    """
    code = models.CharField(max_length=4, unique=True)
    message = models.TextField()

    def __str__(self):
        return f"{self.code}: {self.message}"

class Recipe(TimeStampedMixin, StatusMixin, models.Model):
    """
    Model for recipes. Recipes allow for inheritance, so that a recipe can be 
    just a slight change of a previous one. Inheritance can be:
    - exclusive: when the successor is activates, predecessor is deactivated (not vice versa)
    - non-exclusive: when the successor is activated, predecessor is not deactivated
    Both allow for simultaneous activation of multiple inherited recipes, 
    but exclusive advises agains it.

    Inherits StatusModel

    - name: name of the recipe
    - description: description of the recipe
    - thumbnail: thumbnail of the recipe
    - predecessor: predecessor of the recipe
    - exclusive_inheritance: whether the inheritance is exclusive
    - ingredients: all ingredients of the recipe, specified through IngredientInRecipe model
    - difficulty: difficulty of the recipe
    - cooking_time: time it takes from start to finish
    - active_cooking_time: time it takes to actively cook the recipe
    """

    # General
    
    name = models.CharField(
        max_length=63, 
        verbose_name="Názov"
    )
    description = models.TextField(
        max_length=127, 
        verbose_name="Opis jedla", help_text="Zadajte stručný opis jedla"
    )

    def thumbnail_upload_to(instance, filename):
        return f'recipes/{slugify(instance.__str__())}/thumbnail.{filename.split(".")[1]}'
    thumbnail = models.ImageField(
        upload_to=thumbnail_upload_to, 
        help_text="Pridajte thumbnail", 
        blank=True, null=True
    )

    # Relation to previous
    
    predecessor = models.ForeignKey('self', related_name='successor', 
        on_delete=models.PROTECT, 
        verbose_name='Predchodca', 
        help_text='V prípade, že je tento recept iba pozmenený predchádzajúci, zvolte ktorý mu predchádzal',
        blank=True, null=True,
    )
    exclusive_inheritance = models.BooleanField(
        default=True,
        verbose_name='Deaktivovať predchodcu?',
        help_text='Predchodca bude deaktivovaný až v momente, keď tento recept aktivujete. \
            Toto je vysoko odporúčané, nakoľko hrozia duplicitné recepty v prípade nezaškrtnutia.'
    )

    # Preparation
    
    ingredients = models.ManyToManyField(IngredientVersion, through=IngredientInRecipe, related_name="recipes",
        verbose_name='Ingrediencie',
        help_text="Zvolte všetky ingrediencie",
        blank=True,
    )

    difficulty = models.IntegerField(
        choices=[
            (1, "Easy"),
            (2, "Medium"),
            (3, "Hard"),
            (4, "Profesional"),
        ],
        verbose_name="Náročnosť", help_text="Zadajte náročnosť"
    )
    cooking_time = models.IntegerField(
        validators=[validate_cooking_time_range],
        verbose_name="Čas varenia", help_text="Zadajte dĺžku varenia od začiatku do hotového jedla v minútach"
    )
    active_cooking_time = models.IntegerField(
        validators=[validate_cooking_time_range],
        verbose_name="Aktívny čas varenia", help_text="Zadajte čas, ktorý je potrebné venovať sa vareniu"
    )

    attributes = models.ManyToManyField('recipes.Attribute', related_name="recipes", 
        blank=True,
        verbose_name="Attribúty", help_text="Zadajte všetky atribúty jedla", 
    )
    diet = models.ManyToManyField('recipes.Diet', related_name='recipes',
        blank=True,
        verbose_name="Dieta", help_text="Spadá tento recept do nejakých diet?"
    )
    required_accessories = models.ManyToManyField('recipes.KitchenAccesory', related_name='recipes',
        blank=True,
        verbose_name="Potrebné kuchynské náradie", help_text="Zadajte všetky potrebné kuchynské pomôcky", 
        )

    # Ready to publish checkmarks

    description_finished = models.BooleanField(
        default=False,
        verbose_name='Opis finálne hotový', help_text='Odznačte, ak ešte treba opis jedla prerobiť/opraviť/skontrolovať'
    )
    steps_finished = models.BooleanField(
        default=False,
        verbose_name='Postup finálne hotový', help_text='Odznačte, ak ešte treba postup prerobiť/opraviť'
    )
    ingredients_finished = models.BooleanField(
        default=False,
        verbose_name='Ingrediencie finálne hotové', help_text='Odznačte, ak ešte treba ingrediencie prerobiť/opraviť'
    )

    todo = models.TextField(
        blank=True,
        verbose_name='ToDo poznámka', 
        help_text='Sem napíš všetko, čo ešte pre tento recept nie je hotové. Veci oddeluj enterom.'
    )

    # Cost

    @property
    def cost(self):
        cost = 0
        for ingredient in self.ingredients_mid.all():
            cost += ingredient.cost()
        return cost

    @property
    def cost_str(self):
        return f'{round(self.cost,2)} €'

    price = models.FloatField(
        verbose_name='Predajná cena', help_text=cost, 
        default=None, blank=True, null=True
    )

    @property
    def price_str(self):
        return f'{round(self.price,2)} €'
    
    # Errors

    automatic_errors = models.ManyToManyField('recipes.RecipeError', related_name='recipes',
        blank=True,
        verbose_name="Chyby"
    )

    # ERRORS = (
    #     RecipeError("0", "Missing thumbnail"),
    #     RecipeError("1", "Missing steps"),
    #     RecipeError("2", "Missing ingredients"),
    #     RecipeError("3", "Missing attributes"),
    #     RecipeError("4", "Missing diet"),
    #     RecipeError("5", "ToDo list not empty"),
    # )

    # automatic_errors = models.CharField(max_length=64, default="",
    #     verbose_name="Errors", help_text="String of IDs representing errors separated by commas " + " | ".join([e.__str__() for e in ERRORS]))

    def get_error(self, error_code: str) -> RecipeError:
        """
        Returns a RecipeError object with the corresponding code.
        Raises Exception if code is invalid
        """
        for error in self.ERRORS:
            if error.code is error_code:
                return error
        raise Exception("Invalid error code: %s" % error_code)

    def add_error(self, error_code: str, save=True) -> None:
        error = self.get_error(error_code)
        temp = self.automatic_errors.split(',')
        try:
            temp.remove('')
        except ValueError:
            pass
        temp.append(error.code)
        temp = list(set(temp))
        temp.sort(key=int)
        self.automatic_errors = ",".join(temp)
        if save:
            self.save()

    def remove_error(self, error_code: str, save=True) -> None:
        error = self.get_error(error_code)

        temp = self.automatic_errors.split(',')
        try:
            temp.remove(error.code)
        except ValueError:
            return
        self.automatic_errors = ",".join(temp)
        if save:
            self.save()

    def check_error(self, error_code: str) -> bool:
        """Return True if error is present, False otherwise"""
        error = self.get_error(error_code)

        if error.code in self.automatic_errors.split(','):
            return True
        return False

    def _update_errors(self):
        if not self.thumbnail:
            self.add_error("0", save=False)
        else:
            self.remove_error("0", save=False)

        if self.steps.count() == 0:
            self.add_error("1", save=False)
        else:
            self.remove_error("1", save=False)
        
        if self.ingredients.count() == 0:
            self.add_error("2", save=False)
        else:
            self.remove_error("2", save=False)
        
        if self.attributes.count() == 0:
            self.add_error("3", save=False)
        else:
            self.remove_error("3", save=False)
        
        if self.diet.count() == 0:
            self.add_error("4", save=False)
        else:
            self.remove_error("4", save=False)

        if self.todo != "":
            self.add_error("5", save=False)
        else:
            self.remove_error("5", save=False)
    created_by = models.ForeignKey('accounts.User', related_name="created_recipes", 
        on_delete=models.PROTECT,
        verbose_name="Created by", help_text="Zvolte seba",
    )

    class Meta:
        permissions = [
            ('toggle_recipe_status', 'Can change recipe status'),
        ]

        constraints = [
            # Create a check constraint to ensure that cooking_time is greater than 
            # or equal to active_cooking_time
            models.CheckConstraint(
                check=models.Q(cooking_time__gte=models.F('active_cooking_time')), 
                name='cooking_time_gte_active_cooking_time',
                violation_error_message="Čas varenia musí byť väčší alebo rovný aktívnemu času varenia")
        ]

    @property
    def version(self):
        version = 0
        predecessor = self.predecessor
        while predecessor:
            version += 1
            predecessor = predecessor.predecessor
        return version or None

    def __str__(self):
        result = self.name
        if Recipe.objects.filter(name=self.name).count() > 1:
            result += f" v.{str(self.version)}"
        return result

    def activate(self):
        if self.exclusive_predecessor and self.predecessor:
            self.predecessor.soft_delete()
        super().activate()
    
    
              
    def unique_consecutive_step_numbers(self) -> bool:
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

        # Check if the name is unique
        same_name = Recipe.objects.filter(name=self.name).exclude(pk=self.pk)
        if same_name.count() != 0:
            fam_tree = []
            recipe = self
            while recipe.predecessor:
                fam_tree.append(recipe.predecessor)
            recipe = self
            while recipe.successor:
                fam_tree.append(recipe.successor)

            for recipe in same_name:
                if recipe not in fam_tree:
                    raise ValidationError({'name': 'Meno je už používané receptom, ktorý nieje predchodca ani dedič tohto receptu'})

        # Check if the cooking times are 

        return super().clean()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self._update_errors()
        self.date_modified = timezone.now()
        super().save(*args, **kwargs)
        

class RecipeDeliveryInstance(models.Model):
    recipe = models.ForeignKey('recipes.Recipe', related_name="delivery_days_mid",
        on_delete=models.PROTECT
    )
    delivery_day = models.ForeignKey('deliveries.DeliveryDay', related_name='recipes_mid', 
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
