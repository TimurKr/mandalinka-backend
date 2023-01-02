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
        max_length=255, 
        unique=True,
        verbose_name="Atribút",
    )

    def __str__(self):
        return self.name

class Diet(models.Model):
    name = models.CharField(
        unique=True,
        max_length=32, 
    )

    def __str__(self):
        return self.name


class IngredientInstance(models.Model):
    ingredient = models.ForeignKey("recipes.Ingredient", related_name="instances", 
        on_delete=models.PROTECT
    )
    recipe = models.ForeignKey("recipes.Recipe", related_name="ingredients_mid",
        on_delete=models.PROTECT
    )
    amount = models.IntegerField(
        verbose_name="Množstvo", help_text="Zadajte množstvo danej potraviny"
    )

    def __str__(self):
        return f"{self.amount} {self.ingredient.unit} {self.ingredient.name}"

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

    date_created = models.DateTimeField(auto_now_add=True, verbose_name="Čas vzniku")
    date_modified = models.DateTimeField(auto_now=True, verbose_name="Naposledy upravené")

    class Meta:
        permissions = [
            ('toggle_is_active_ingredient', 'Can activate or deactivate any ingredient'),
        ]

    def __str__(self):
        return self.name

    def activate(self):
        self.is_active = True
        self.save()
    
    def deactivate(self):
        self.is_active = False
        self.save()


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
    thumbnail = models.ImageField(
        upload_to="recipes", 
        help_text="Pridajte thumbnail", 
        blank=True, null=True
    )
    is_active = models.BooleanField(
        default=False, editable=False,
        verbose_name="Aktívny", help_text="Používa sa tento recept ešte?"
    )

    # Relation to previous
    predecessor = models.ForeignKey('recipes.Recipe', related_name='successor', 
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
    StF_cooking_time = models.IntegerField(
        validators=[validate_cooking_time_range],
        verbose_name="Čas varenia", help_text="Zadajte dĺžku varenia od začiatku do hotového jedla"
    )
    active_cooking_time = models.IntegerField(
        validators=[validate_cooking_time_range],
        verbose_name="Čas prípravy", help_text="Zadajte dĺžku aktívneho času varenia"
    )

    attributes = models.ManyToManyField('recipes.Attribute', related_name="recipes", 
        blank=True,
        verbose_name="Attribúty", help_text="Zadajte všetky atribúty jedla", 
    )
    
    diet = models.ManyToManyField('recipes.Diet', related_name='recipes',
        blank=True,
        verbose_name="Dieta", help_text="Spadá tento recept do nejakých diet?"
    )


    date_created = models.DateTimeField(auto_now_add=True, verbose_name="Čas vzniku")
    date_modified = models.DateTimeField(auto_now=True, verbose_name="Naposledy upravené")
    created_by = models.ForeignKey('accounts.User', related_name="created_recipes", 
        on_delete=models.PROTECT,
        verbose_name="Created by", help_text="Zvolte seba",
    )

    class Meta:
        permissions = [
            ('toggle_is_active_recipe', 'Can activate or deactivate any recipe'),
        ]

    def __str__(self):
        return f"{self.name}"

    def activate(self):
        self.is_active = True
        if self.exclusive_predecessor and self.predecessor:
            self.predecessor.deactivate()
        self.save()
    
    def deactivate(self):
        self.is_active = False
        self.save()
        

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