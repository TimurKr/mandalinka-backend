from django.db import models
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from utils.validators import validate_positivity

from ingredients.models import Ingredient, IngredientVersion
from utils.models import StatusMixin, Unit, TimeStampedMixin

from django.db.models.signals import post_save
from django.dispatch import receiver
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


class RecipeDesignIngredient(TimeStampedMixin, models.Model):
    """
    Model for ingredient use in RecipeDesign.
    `alternative_for` is used to represent alternative ingredients. The default 
    ingredient is the one with alternative_for set to None.
    """

    # Fields to overwrite
    ingredient = models.ForeignKey(Ingredient, related_name="recipe_designs", 
        on_delete=models.CASCADE
    )
    recipe_design = models.ForeignKey('recipes.RecipeDesign', related_name="ingredients",
        on_delete=models.CASCADE
    )

    alternative_for = models.ForeignKey('self', related_name="alternatives",
        on_delete=models.CASCADE, blank=True, null=True)

    amount = models.FloatField(
        verbose_name="Množstvo", help_text="Zadajte množstvo danej potraviny na dve porcie",
        validators=(validate_positivity,)
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
        unique_together = ('ingredient', 'recipe_design')


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

    recipe = models.ForeignKey('RecipeDesign', 
        on_delete=models.CASCADE, related_name="steps"
    )

    def __str__(self):
        return f'{self.recipe} step n. {self.number}: {self.text}'

class RecipeDesignError(models.Model):
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

    attributes = models.ManyToManyField(Attribute, related_name="recipes", 
        blank=True,
        verbose_name="Attribúty", help_text="Zadajte všetky atribúty jedla", 
    )
    diet = models.ManyToManyField(Diet, related_name='recipes',
        blank=True,
        verbose_name="Dieta", help_text="Spadá tento recept do nejakých diet?"
    )
    required_accessories = models.ManyToManyField(KitchenAccesory, related_name='recipes',
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
    def cost(self) -> float:
        cost = 0
        for ingredient in self.ingredients.all():
            cost += ingredient.ingredient.cost
        return cost

    @property
    def cost_str(self) -> str:
        return f'{round(self.cost,2)} €'

    price = models.FloatField(
        verbose_name='Predajná cena', 
        default=None, blank=True, null=True
    )

    @property
    def price_str(self) -> str:
        return f'{round(self.price,2)} €'
    
    # Errors

    _automatic_errors = models.ManyToManyField('recipes.RecipeDesignError', related_name='recipes',
        blank=True,
        verbose_name="Chyby"
    )

    def has_error(self, error=None, code=None) -> bool:
        """Check if given error or code is valid and 
        returns True or False if given error is in this recipe's errors"""
        if not error and not code:
            raise ValueError("Either error or code must be provided")
        if not error:
            try:
                error = RecipeDesignError.objects.get(code=code)
            except RecipeDesignError.DoesNotExist:
                raise ValueError("Code does not exist")

        return self._automatic_errors.filter(code=code).exists()


    def add_error(self, error=None, code=None, save=True) -> None:
        if self.has_error(error, code):
            return
        error = error or RecipeDesignError.objects.get(code=code)
        self.automatic_errors.add(error)
        if save:
            self.save()

    def remove_error(self, error=None, code=None, save=True) -> None:
        if not self.has_error(error, code):
            return
        error = error or RecipeDesignError.objects.get(code=code)
        self.automatic_errors.remove(error)
        if save:
            self.save()

    def _update_auto_errors(self):
        thumbnail_error = RecipeDesignError.objects.get_or_create(
            code='0', message='Chýba thumbnail')
        steps_error = RecipeDesignError.objects.get_or_create(
            code='1', message='Chýba postup')
        ingredients_error = RecipeDesignError.objects.get_or_create(
            code='2', message='Chýbajú ingrediencie')
        attributes_error = RecipeDesignError.objects.get_or_create(
            code='3', message='Chýbajú atribúty')
        diet_error = RecipeDesignError.objects.get_or_create(
            code='4', message='Chýbajú diety')
        todo_error = RecipeDesignError.objects.get_or_create(
            code='5', message='Zostáva ToDo list')

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

        for error in RecipeDesignError.objects.all():
            if self.has_error(error):
                result += f'{error.message}, '

        if result:
            result = result[:-2]

        return result

    created_by = models.ForeignKey('accounts.User', related_name="created_recipes", 
        on_delete=models.PROTECT,
        verbose_name="Created by", help_text="Zvolte seba",
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


    class Meta:
        permissions = [
            ('change_recipe_status', 'Can change recipe status'),
        ]

        constraints = [
            # Create a check constraint to ensure that cooking_time is greater than 
            # or equal to active_cooking_time
            models.CheckConstraint(
                check=models.Q(cooking_time__gte=models.F('active_cooking_time')), 
                name='cooking_time_gte_active_cooking_time',
                violation_error_message="Čas varenia musí byť väčší alebo rovný aktívnemu času varenia")
        ]

        ordering = ['-status_changed', '-created']


    def __str__(self):
        result = self.name
        version = self.version
        if version:
            result += f" v.{str(self.version)}"
        return result

    def clean(self) -> None:

        # Check if the name is unique, except if it is inherited
        same_name = RecipeDesign.objects.filter(name=self.name).exclude(pk=self.pk)
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
                    raise ValidationError({'name': 'Meno je už používané receptom, ktorý nieje predchodca ani dedič tohto receptu'})

        return super().clean()

@receiver(post_save, sender=RecipeDesign)
def update_recipe_errors(sender, instance, created, **kwargs):
    instance._update_errors()
        

class RecipeIngredient(TimeStampedMixin, models.Model):
    """
    Model for archiving ingredient uses in recipes (for history).
    """
    ingredient = models.ForeignKey(IngredientVersion, related_name="recipes", 
        on_delete=models.CASCADE
    )
    recipe = models.ForeignKey('recipes.RecipeDeliveryInstance', related_name="ingredients",
        on_delete=models.CASCADE
    )

class RecipeDeliveryInstance(models.Model):
    recipe_design = models.ForeignKey(RecipeDesign, related_name="delivery_days",
        on_delete=models.PROTECT
    )
    delivery_day = models.ForeignKey('deliveries.DeliveryDay', related_name='recipes', 
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
        unique_together = ('recipe_design', 'delivery_day')