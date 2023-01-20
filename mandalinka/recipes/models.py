from django.db import models
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

import datetime



################################# Validators ###################################

def validate_cooking_time_range(value):
    if value >= 300 or value < 1:
        raise ValidationError(
            _('%(value)s is not in the required cooking range [1, 300]'),
            params = {'value': value},
        )

def validate_positivity(value):
    if value <= 0:
        raise ValidationError(
            _('%(value)s is not positive'),
            params = {'value': value},
        )

################################# Models ###################################

class Alergen(models.Model):
    name = models.CharField(
        unique = True,
        max_length=63, 
        verbose_name="Alergén"
    )
    code = models.IntegerField(
        primary_key=True, 
        verbose_name="Kód"
    )

    def __str__(self):
        return f"{self.code}: {self.name}"

class Attribute(models.Model):
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


class Unit(models.Model):
    name = models.CharField(
        unique=True,
        max_length=64, 
    )

    sign = models.CharField(
        unique=True,
        max_length=6, 
    )

    base_unit = models.ForeignKey('self', 
        blank=True, null=True,
        on_delete=models.RESTRICT,
        related_name='sub_units'
    )

    conversion_rate = models.DecimalField(
        max_digits=13, decimal_places=6,
        verbose_name="Konštanta na premenu na base_unit"
    )

    class Systems:
        METRIC = 'METRIC'
        IMPERIAL = 'IMPERIAL'
        options = (
            (METRIC, METRIC),
            (IMPERIAL, IMPERIAL)
        )

    system = models.CharField(
        max_length=8, 
        choices=Systems.options, default=Systems.METRIC
    )

    def __str__(self) -> str:
        return f'{self.sign}'

    def in_base(self, amount: float, as_string: bool = False):
        value = amount * float(self.conversion_rate)
        if as_string:
            return f'{value} {self.base}'
        else:
            return value
    
    def from_base(self, amount: float, as_string: bool = False):
        value = amount / float(self.conversion_rate)
        if as_string:
            return f'{value} {self.base}'
        else:
            return value


class Ingredient(models.Model):
    """
    Base class for ingredient, whenever we are choosing an ingredient, we are choosing form this model.
    Each Ingredient can have multiple IngredientVersions, but only one active one.
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

    alergens = models.ManyToManyField('recipes.Alergen', related_name="ingredients",
        blank=True, default=None,
        verbose_name="Alergény", help_text="Zvolte všetky alergény"
    )

    unit = models.ForeignKey('Unit', related_name='uses',
        on_delete=models.PROTECT, default=1
    )

    date_created = models.DateTimeField(auto_now_add=True, verbose_name="Čas vzniku")
    date_modified = models.DateTimeField(auto_now=True, verbose_name="Naposledy upravené")

    def __str__(self):
        return self.name

    def active_version(self):
        return self.versions.filter(is_active=True).first()
        
    def is_active(self) -> bool:
        if self.versions.filter(is_active=True).exists():
            return True
        return False


class IngredientVersion(models.Model):
    """
    Model for a version of an object. After activation should't be changed 
    and a new version should be created.
    """

    parent = models.ForeignKey('Ingredient', related_name='versions',
        on_delete=models.RESTRICT
    )

    # Status manipulation
    class Statuses:
        """Class containing all possible statuses"""
        ACTIVE = "Active"
        PREPARATION = "Preparation"
        RETIRED = "Retired"
        options = (
            (PREPARATION, PREPARATION),
            (ACTIVE, ACTIVE),
            (RETIRED, RETIRED)
        )

    status = models.CharField(
        max_length=20, 
        choices=Statuses.options, default=Statuses.PREPARATION,
        editable=False
    )
    last_status_change = models.DateTimeField(editable=False, auto_now_add=True)

    def is_active(self):
        return self.status == self.Statuses.ACTIVE

    def activate(self):
        """
        Activate this version and deactivate all other ones
        Always use this method to change the status to active!!!
        Warning, changes all IngredientInRecipe to use the new active instead of the old one
        """
        for v in self.parent.versions.filter(status=self.Statuses.ACTIVE):
            v.retire()
            for i in v.instances:
                if i.recipe.is_active():
                    i.ingredient = self
                    i.save()

        self.status = self.Statuses.ACTIVE
        self.last_status_change = timezone.now()
        self.save()

    def retire(self):
        self.status = self.Statuses.RETIRED
        self.last_status_change = timezone.now()
        self.save()

    
    cost = models.FloatField(
        verbose_name="Cena na jednotku", help_text="Zadajte cenu na zvolenú jednotku"
    )

    def print_cost(self):
        return f'{round(self.cost,2)} €'

    source = models.CharField(max_length=64, help_text="Toto ešte bude raz foreign key na dodávatela")

    date_created = models.DateTimeField(auto_now_add=True, verbose_name="Čas vzniku")
    date_modified = models.DateTimeField(auto_now=True, verbose_name="Naposledy upravené")

    class Meta:
        permissions = [
            ('toggle_is_active_ingredient', 'Can activate or deactivate any ingredient'),
        ]

    def unit(self):
        return self.parent.unit

    def version_number(self):
        return self.parent.versions.filter(date_created__lt=self.date_created).count()

    def save(self, *args, **kwargs):
        if self.is_active() and self.parent.versions.filter(status=self.Statuses.ACTIVE).exclude(pk=self.pk).exists():
            raise ValueError(f'There already is an active version of the ingredient "{self.parent}"')
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return f'{self.parent} v.{self.version_number()} - {self.status}'

class IngredientInRecipe(models.Model):
    ingredient = models.ForeignKey(IngredientVersion, related_name="recipes_mid", 
        on_delete=models.CASCADE
    )
    recipe = models.ForeignKey("recipes.Recipe", related_name="ingredients_mid",
        on_delete=models.CASCADE
    )
    amount = models.FloatField(
        verbose_name="Množstvo", help_text="Zadajte množstvo danej potraviny na dve porcie",
        validators=(validate_positivity,)
    )

    def unit(self):
        return self.ingredient.unit

    def cost(self):
        return self.amount * self.ingredient.cost

    def print_cost(self):
        return f'{round(self.cost(), 2)} €'
    
    def __str__(self):
        return f"{self.amount} {self.unit()} {self.ingredient} in {self.recipe}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.recipe.save()


class Step(models.Model):

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

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.recipe.save()

class Recipe(models.Model):
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
    exclusive_predecessor = models.BooleanField(
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

    def cost(self):
        cost = 0
        for ingredient in self.ingredients_mid.all():
            cost += ingredient.cost()
        return cost

    def print_cost(self):
        return f'{round(self.cost(),2)} €'

    price = models.FloatField(
        verbose_name='Predajná cena', help_text=cost, 
        default=None, blank=True, null=True
    )

    def print_price(self):
        return f'{round(self.price,2)} €'

    todo = models.TextField(
        blank=True, 
        verbose_name='ToDo poznámka', 
        help_text='Sem napíš všetko, čo ešte pre tento recept nie je hotové. Veci oddeluj enterom.'
    )

    class Statuses:
        """Class containing all possible statuses"""
        PREPARATION = "Preparation"
        ACTIVE = "Active"
        RETIRED = "Retired"
        options = (
            (PREPARATION, PREPARATION),
            (ACTIVE, ACTIVE),
            (RETIRED, RETIRED)
        )

    status = models.CharField(choices=Statuses.options, default=Statuses.PREPARATION,
        max_length=20,
        editable=False
    )
    last_status_change = models.DateTimeField(editable=False, auto_now_add=True)

    class RecipeError:
        def __init__(self, code, text):
            self.code = code
            self.text = text

        def __str__(self):
            return f"{self.code}: {self.text}"

        def __repr__(self):
            return self.__str__()

    ERRORS = (
        RecipeError("0", "Missing thumbnail"),
        RecipeError("1", "Missing steps"),
        RecipeError("2", "Missing ingredients"),
        RecipeError("3", "Missing attributes"),
        RecipeError("4", "Missing diet"),
        RecipeError("5", "ToDo list not empty"),
    )

    automatic_errors = models.CharField(max_length=64, default="",
        verbose_name="Errors", help_text=f"String of IDs representing errors separated by commas " + " | ".join([e.__str__() for e in ERRORS]))



    date_created = models.DateTimeField(auto_now_add=True, verbose_name="Čas vzniku")
    date_modified = models.DateTimeField(auto_now=True, verbose_name="Naposledy upravené")
    created_by = models.ForeignKey('accounts.User', related_name="created_recipes", 
        on_delete=models.PROTECT,
        verbose_name="Created by", help_text="Zvolte seba",
    )

    class Meta:
        permissions = [
            ('toggle_recipe_status', 'Can change recipe status'),
        ]

        constraints = [
            models.CheckConstraint(
                check=models.Q(cooking_time__gte=models.F('active_cooking_time')), 
                name='cooking_time_gte_active_cooking_time',
                violation_error_message="Čas varenia musí byť väčší alebo rovný aktívnemu času varenia")
        ]
    

    def __str__(self):
        result = f"{self.name}"
        if Recipe.objects.filter(name=self.name).count() > 1:
            version = 1
            predecessor = self.predecessor
            while predecessor:
                version += 1
                predecessor = predecessor.predecessor
            result += f" v.{str(version)}"
        return result

    def activate(self):
        self.status = self.Statuses.ACTIVE
        if self.exclusive_predecessor and self.predecessor:
            self.predecessor.retire()
        self.last_status_change = timezone.now()
        self.save()
    
    def retire(self):
        self.status = self.Statuses.RETIRED
        self.last_status_change = timezone.now()
        self.save()

    def deactivate(self):
        self.status = self.Statuses.PREPARATION
        self.last_status_change = timezone.now()
        self.save()

    def is_active(self) -> bool:
        if self.status is self.Statuses.ACTIVE:
            return True
        return False


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
