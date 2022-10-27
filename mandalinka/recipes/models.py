from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

################################# Validators ###################################

def validate_cooking_time_range(value):
    if value > 300 or value < 1:
        raise ValidationError(
            _('%(value)s is not in the required cooking range'),
            params = {'value': value},
        )

def validate_portions(value):
    if value % 2 != 0 or value < 0 or value > 100:
        raise ValidationError(
            _('%(value)s is invalid amount of portions, should be even and on range 0<=x<=100]')
        )



################################# Models ###################################

class Alergen(models.Model):
    name = models.CharField(
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
        max_length=255, 
        primary_key=True,
        verbose_name="Atribút",
    )

    def __str__(self):
        return self.name

class Diet(models.Model):
    name = models.CharField(
        max_length=32, 
        primary_key=True, 
        verbose_name="Patrí toto jedlo do nejakej diety",
    )

    def __str__(self):
        return self.name


class IngredientInstance(models.Model):
    ingredient = models.ForeignKey("recipes.Ingredient", on_delete=models.PROTECT)
    recipe_version = models.ForeignKey("recipes.Recipe", on_delete=models.PROTECT)
    amount = models.IntegerField(
        verbose_name="Množstvo", help_text="Zadajte množstvo danej potraviny"
    )

    def __str__(self):
        return f"{self.amount} {self.ingredient.unit} {self.ingredient}"

class Ingredient(models.Model):
    title = models.CharField(
        max_length=31, unique=True, 
        verbose_name="Názov", help_text="Názov ingrediencie"
    )
    price_per_unit = models.FloatField(
        verbose_name="Cena na jednotku", help_text="Zadajte cenu na nižšie zvolenú jednotku"
    )

    img = models.ImageField(
        upload_to="ingredients", 
        verbose_name="Obrázok", help_text="Pridajte obrazok ku kroku",
        blank=True, null=True, default=None
    )
    
    UNITS_TO_SELECT = [
        (None, "Zvolte jednotku"),
        ("g", "gramy"),
        ("ml", "mililitre"),
        ("ks", "kusy"), 
        ]
    unit = models.CharField(
        max_length=3, choices=UNITS_TO_SELECT, 
        verbose_name="Jednotka", help_text="Zvolte jednotku")

    alergens = models.ManyToManyField('recipes.Alergen', related_name="ingredients",
        blank=True, 
        verbose_name="Alergény", help_text="Zvolte všetky alergény:"
    )

    date_created = models.DateTimeField(auto_now_add=True, verbose_name="Čas vzniku")
    date_modified = models.DateTimeField(auto_now=True, verbose_name="Naposledy upravené")

    def __str__(self):
        return self.title


class Recipe(models.Model):
    # General
    title = models.CharField(max_length=63, unique=True, verbose_name="Názov")
    description = models.TextField(max_length=127, verbose_name="Opis jedla", help_text="Zadajte stručný opis jedla")
    thumbnail = models.ImageField(
        upload_to="recipes", 
        help_text="Pridajte thumbnail", 
        blank=True, null=True)
    active = models.BooleanField(
        verbose_name="Aktívny",
        blank=True,
    )

    # Relation to previous
    predecessor = models.ForeignKey('recipes.Recipe', related_name='successor', 
        on_delete=models.PROTECT, 
        verbose_name='predchodca', 
        help_text='V prípade, že je tento recept iba pozmenený predchádzajúci, zvolte ktorý mu predchádzal',
        blank=True
    )

    # Preparation

    ingredients = models.ManyToManyField('recipes.Ingredient', through='recipes.IngredientInstance', related_name="recipes",
        verbose_name='Ingrediencie',
        help_text="Zvolte všetky ingrediencie",
    )
    steps = models.TextField(blank=True, max_length=1024, 
        verbose_name="Postup", help_text='Jednotlivé kroky oddelujte enterom')

    difficulty = models.IntegerField(
        choices=[
            (1, "Easy"),
            (2, "Medium"),
            (3, "Hard"),
            (4, "Profesional"),
        ],
        verbose_name="Náročnosť", help_text="Zadajte náročnosť"
    )
    StF_time = models.IntegerField(
        validators=[validate_cooking_time_range],
        verbose_name="Čas varenia", help_text="Zadajte dĺžku varenia od začiatku do hotového jedla"
    )
    active_time = models.IntegerField(
        validators=[validate_cooking_time_range],
        verbose_name="Čas prípravy", help_text="Zadajte dĺžku aktívneho času varenia"
    )

    attributes = models.ManyToManyField('recipes.Attribute', related_name="recipes", 
        blank=True,
    )
    
    diet = models.ManyToManyField('recipes.Diet', 
        related_name='recipes',
    )


    date_created = models.DateTimeField(auto_now_add=True, verbose_name="Čas vzniku")
    date_modified = models.DateTimeField(auto_now=True, verbose_name="Naposledy upravené")
    created_by = models.ForeignKey('accounts.User', related_name="created_recipes", 
        on_delete=models.PROTECT,
        verbose_name="Created by", help_text="Zvolte seba",
        blank=True, null=True
    )

    def __str__(self):
        return f"{self.title}"
