from django.db import models
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
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

class IngredientInstance(models.Model):
    ingredient = models.ForeignKey("recipes.Ingredient", related_name="instances", 
        on_delete=models.PROTECT
    )
    recipe = models.ForeignKey("recipes.Recipe", related_name="ingredients_mid",
        on_delete=models.CASCADE
    )
    amount = models.IntegerField(
        verbose_name="Množstvo", help_text="Zadajte množstvo danej potraviny na dve porcie",
        validators=(validate_positivity,)
    )

    def __str__(self):
        return f"{self.amount} {self.ingredient.unit} {self.ingredient.name}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.recipe.save()


class Ingredient(models.Model):
    name = models.CharField(
        max_length=31, 
        unique=True,
        verbose_name="Názov", help_text="Názov ingrediencie"
    )
    img = models.ImageField(
        upload_to="ingredients", 
        verbose_name="Obrázok", help_text="Pridajte obrazok ku kroku",
        blank=True, null=True, default=None
    )
    is_active = models.BooleanField(
        default=False, editable=False,
        verbose_name="Aktívny", help_text="Používa sa táto ingrediencia ešte?"
    )

    UNITS_TO_SELECT = [
        (None, "Zvolte jednotku"),
        ("g", "Gram"),
        ("ml", "Mililiter"),
        ("ks", "Kus"), 
        ]
    unit = models.CharField(
        max_length=3, choices=UNITS_TO_SELECT, 
        verbose_name="Jednotka", help_text="Zvolte jednotku")
    price_per_unit = models.FloatField(
        verbose_name="Cena na jednotku", help_text="Zadajte cenu na zvolenú jednotku"
    )

    alergens = models.ManyToManyField('recipes.Alergen', related_name="ingredients",
        blank=True, default=None,
        verbose_name="Alergény", help_text="Zvolte všetky alergény"
    )

    class Statuses:
        PREPARATION = "Preparation"
        ACTIVE = "Active"
        RETIRED = "Retired"
        options = (
            (PREPARATION, PREPARATION),
            (ACTIVE, ACTIVE),
            (RETIRED, RETIRED)
        )

    status = models.CharField(max_length=20, choices=Statuses.options, default=Statuses.PREPARATION)
    last_status_change = models.DateTimeField(editable=False, auto_now_add=True)

    date_created = models.DateTimeField(auto_now_add=True, verbose_name="Čas vzniku")
    date_modified = models.DateTimeField(auto_now=True, verbose_name="Naposledy upravené")

    class Meta:
        permissions = [
            ('toggle_is_active_ingredient', 'Can activate or deactivate any ingredient'),
        ]

    def __str__(self):
        return f"{self.name} [{self.unit}]"

    def activate(self):
        self.is_active = True
        self.save()
    
    def deactivate(self):
        self.is_active = False
        self.save()

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
    ingredients = models.ManyToManyField('recipes.Ingredient', through='recipes.IngredientInstance', related_name="recipes",
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

    todo = models.TextField(
        blank=True, 
        verbose_name='ToDo poznámka', 
        help_text='Sem napíš všetko, čo ešte pre tento recept nie je hotové. Veci oddeluj enterom.'
    )

    class Statuses:
        PREPARATION = "Preparation"
        ACTIVE = "Active"
        RETIRED = "Retired"
        options = (
            (PREPARATION, PREPARATION),
            (ACTIVE, ACTIVE),
            (RETIRED, RETIRED)
        )

    status = models.CharField(max_length=20, choices=Statuses.options, default=Statuses.PREPARATION)
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
        self.last_status_change = datetime.datetime.now()
        self.save()
    
    def retire(self):
        self.status = self.Statuses.RETIRED
        self.last_status_change = datetime.datetime.now()
        self.save()

    def deactivate(self):
        self.status = self.Statuses.PREPARATION
        self.last_status_change = datetime.datetime.now()
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
        self.date_modified = datetime.datetime.now()
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
