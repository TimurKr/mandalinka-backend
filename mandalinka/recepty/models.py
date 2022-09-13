from enum import unique
from pyexpat import model
from django.db import models
from django.core.validators import RegexValidator
from home.models import Food_attr

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
    recipe = models.ForeignKey("RecipeVersion", on_delete=models.CASCADE)
    amount = models.IntegerField(verbose_name="Množstvo", help_text="Zadajte množstvo danej potraviny")

    def __str__(self):
        return f"{self.amount} {self.ingredient.unit} {self.ingredient}"

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

    date_created = models.DateTimeField(auto_now_add=True, verbose_name="Čas vzniku")
    date_modified = models.DateTimeField(auto_now=True, verbose_name="Naposledy upravené")

    def __str__(self):
        return f"{self.title}"

class Step(models.Model):
    step = models.TextField(max_length=250, help_text="Krok: ")
    step_img = models.ImageField(upload_to=f"recepty/static/photos/", help_text="Pridajte obrazok ku kroku", default=None)
    step_no = models.IntegerField(verbose_name="Krok cislo:", help_text="Zadaj poradie kroku")
    recipe = models.ForeignKey("RecipeVersion", on_delete=models.CASCADE, related_name="Steps", null=True, blank=True)
    
    date_modified = models.DateTimeField(auto_now=True, verbose_name="Naposledy upravené")

    # class Meta:
    #     # ensuring each recipe has only one unique step_no
    #     constraints = [
    #         models.UniqueConstraint(fields=['recipe','step_no'], name='unique_step_number')
    #     ]

    def __str__(self):
        return f"text: {self.step}"

class Recipe(models.Model):
    title = models.CharField(max_length=63, unique=True, help_text="Názov receptu")
    description = models.TextField(max_length=127, verbose_name="Opis jedla", help_text="Zadajte stručný opis jedla")
    thumbnail = models.ImageField(upload_to=f"recepty/static/photos/", help_text="Pridajte thumbnail", default=None)
    active = models.BooleanField(default=True, verbose_name="Aktívny")

    attributes = models.ManyToManyField(Food_attr)

    date_created = models.DateTimeField(auto_now_add=True, verbose_name="Čas vzniku")
    date_modified = models.DateTimeField(auto_now=True, verbose_name="Naposledy upravené")

    def __str__(self):
        return f"{self.title}"

    def cost(self):
        # Needs attention
        pass

    def deactivate():
        # deactivates all of its verions
        pass

class RecipeVersion(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="recipe_versions")
    version = models.IntegerField(verbose_name="Verzia receptu", help_text="Zadajte koľkatá je to verzia receptu")
    prep_time = models.IntegerField(verbose_name="Čas prípravy", help_text="Zadajte dĺžku prípravy")
    ingredients = models.ManyToManyField(Ingredient, through=IngredientInstance, help_text="Zvolte všetky ingrediencie", related_name="recipes")
    steps = models.ManyToManyField(Step, blank=True, verbose_name="Kroky", help_text="Pridajte kroky", related_name="recipes")

    date_created = models.DateTimeField(auto_now_add=True, verbose_name="Čas vzniku")
    date_modified = models.DateTimeField(auto_now=True, verbose_name="Naposledy upravené")
    
    active = models.BooleanField(default=True, verbose_name="Aktívny")

    def __str__(self):
        return f"{self.recipe} v.{self.version}"

    def avg_rating(self):
        rating_sum = 0
        rating_num = 0
        for recipeuse in self.uses.all():
            for r in recipeuse.ratings.all():
                if r.taste:
                    rating_sum += int(r.amount)
                    rating_num += 1
        if rating_num:
            return rating_sum/rating_num
        return "No ratings"

class RecipeInstance(models.Model):
    recipe_version = models.ForeignKey(RecipeVersion, on_delete=models.PROTECT, related_name="uses")
    date_to_be_used = models.DateField()

    date_created = models.DateTimeField(auto_now_add=True, verbose_name="Čas vzniku")
    date_modified = models.DateTimeField(auto_now=True, verbose_name="Naposledy upravené")

    def __str__(self):
        return f"{self.recipe_version} zo dňa {self.date_to_be_used}"


class Rating(models.Model):
    recipe_instance = models.ForeignKey(RecipeInstance, on_delete=models.CASCADE, related_name="ratings")

    choices_amount = [("1", "Porcia bola malá"),
        ("2", "Porcia mohla byť trochu väčšia"), 
        ("3", "Porcia bola akurát"),
        ("4", "Stačilo by trochu menej"),
        ("5", "Porcia bola príliš veľká")]
    amount = models.CharField(blank=True, default=None, null=True, max_length=1, choices=choices_amount, verbose_name="Hodnotenie množstva", help_text="Sedelo množstvo jedla s objednanou porciou?")
    
    choices_stars = [("1", "1"), 
        ("2", "2"), 
        ("3", "3"), 
        ("4", "4"), 
        ("5", "5")]
    taste = models.CharField(blank=True, default=None, null=True, max_length=1, choices=choices_stars, verbose_name="Chuť", help_text="Viac je lepšie")
    delivery = models.CharField(blank=True, default=None, null=True, max_length=1, choices=choices_stars, verbose_name="Doručenie", help_text="Viac je lepšie")
    
    date_created = models.DateTimeField(auto_now_add=True, verbose_name="Čas vzniku")
    date_modified = models.DateTimeField(auto_now=True, verbose_name="Naposledy upravené")

    def __str__(self):
        amount = '*' * int(self.amount)
        taste = '*' * int(self.taste)
        delivery = '*' * int(self.delivery)
        return f"Množstvo: {amount}\nChuť: {taste}\nMnožstvo {delivery}"

