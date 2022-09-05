from enum import unique
from pyexpat import model
from django.db import models
from django.core.validators import RegexValidator

# Create your models here.
# class Address(models.Model):
#     street = models.CharField(max_length=63, verbose_name="Ulica", help_text="Zadajte ulicu a číslo")
#     postal_code = models.CharField(max_length=5, verbose_name="PSČ", help_text="Zadajte poštovné smerovacie číslo")
#     city = models.CharField(max_length=31, verbose_name="Mesto", help_text="Zadajte mesto")
#     COUNTIRES_TO_SELECT = [
#         ("", "Zvoľte krajinu"),
#         ("SK", "Slovensko"),
#         ("CZ", "Česká Republika"),
#         ("Iné", "Iné")
#     ]
#     country = models.CharField(
#         max_length=3, 
#         choices=COUNTIRES_TO_SELECT, verbose_name="Krajina", help_text="Zvolte krajinu")

# class Contact(models.Model):
#     address = models.ForeignKey(Address, on_delete=models.PROTECT, verbose_name="Adresa", help_text="Zvolte adresu")
#     email = models.EmailField(blank=False, verbose_name="Email", help_text="Zadajte e-mail")
#     website = models.URLField(verbose_name="Webstránka", help_text="Zadajte link na webstránku dodávatela")
#     phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
#     phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True) # Validators should be a list


# class Supplier(models.Model):
#     title = models.CharField(max_length=63, unique=True, primary_key=True, verbose_name="Názov", help_text="Názov dodávatela")
#     contact = models.ForeignKey(Address, on_delete=models.PROTECT, blank=True, help_text="Zvoľte kontakt na dodávatela")


class Alergen(models.Model):
    title = models.CharField(max_length=63, verbose_name="Alergén")
    code = models.IntegerField(primary_key=True, verbose_name="Kód alergénu")

    def __str__(self):
        return f"{self.code}: {self.title}"


class IngredientInstance(models.Model):
    ingredient = models.ForeignKey("Ingredient", on_delete=models.PROTECT)
    recipe = models.ForeignKey("Recipe", on_delete=models.CASCADE)
    amount = models.IntegerField(primary_key=True, verbose_name="Množstvo", help_text="Zadajte množstvo danej potraviny")


class Ingredient(models.Model):
    title = models.CharField(max_length=31, unique=True, verbose_name="Názov", help_text="Názov ingrediencie")
    # supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT, verbose_name="Dodávateľ", help_text="Zvolte dodávateľa")
    price_per_unit = models.FloatField(verbose_name="Cena na jednotku", help_text="Zadajte cenu na nižšie zvolenú jednotku")
    
    UNITS_TO_SELECT = [
        ("", "Zvolte jednotku"),
        ("g", "gramy"),
        ("ml", "mililitre"),
        ("ks", "kusy"), 
        ]
    unit = models.CharField(max_length=3, choices=UNITS_TO_SELECT, verbose_name="Jednotka", help_text="Zvolte jednotku")

    alergens = models.ManyToManyField(Alergen, blank=True, help_text="Zvolte všetky alergény:", verbose_name="Alergény", related_name="Ingredients")

    def __str__(self):
        return f"{self.title}"

class Step(models.Model):
    step = models.TextField(max_length=250, help_text="Krok: ")
    step_img = models.ImageField(upload_to=f"recepty/static/photos/", help_text="Pridajte obrazok ku kroku", default=None)
    step_no = models.IntegerField(verbose_name="Krok cislo:", help_text="Zadaj poradie kroku")
    recipe = models.ForeignKey("Recipe", on_delete=models.CASCADE, related_name="Recipes", null=True, blank=True)
    
    class Meta:
        # ensuring each recipe has only one unique step_no
        constraints = [
            models.UniqueConstraint(fields=['step_no', 'recipe'], name='Each recipe has a unique set of steps')
        ]
    def __str__(self):
        return f"text: {self.step}"

class Recipe(models.Model):
    title = models.CharField(max_length=63, unique=True, help_text="Názov receptu")
    description = models.TextField(max_length=127, verbose_name="Opis jedla", help_text="Zadajte stručný opis jedla")
    prep_time = models.IntegerField(verbose_name="Čas prípravy", help_text="Zadajte dĺžku prípravy")
    ingredients = models.ManyToManyField(Ingredient, through=IngredientInstance, blank=False, help_text="Zvolte všetky ingrediencie", related_name="recipes")
    thumbnail = models.ImageField(upload_to=f"recepty/static/photos/", help_text="Pridajte thumbnail", default=None)

    steps = models.ManyToManyField(Step, blank=False, help_text="Pridajte kroky", related_name="recipes")

    # Price

    def __str__(self):
        return f"{self.title}"
