from enum import unique
from pyexpat import model
from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.apps import apps
from mandalinka import constants


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
    title = models.CharField(
        max_length=63, 
        verbose_name="Alergén"
    )
    code = models.IntegerField(
        primary_key=True, 
        verbose_name="Kód alergénu"
    )

    def __str__(self):
        return f"{self.code}: {self.title}"


class FoodAttribute(models.Model):
    attr = models.CharField(max_length=255)

    def __str__(self):
        return self.attr

class IngredientInstance(models.Model):
    ingredient = models.ForeignKey("Ingredient", on_delete=models.PROTECT)
    recipe_version = models.ForeignKey("RecipeVersion", on_delete=models.CASCADE)
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
    # supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT, verbose_name="Dodávateľ", help_text="Zvolte dodávateľa")
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

    alergens = models.ManyToManyField(Alergen, related_name="ingredients",
        blank=True, 
        verbose_name="Alergény", help_text="Zvolte všetky alergény:"
    )

    date_created = models.DateTimeField(auto_now_add=True, verbose_name="Čas vzniku")
    date_modified = models.DateTimeField(auto_now=True, verbose_name="Naposledy upravené")

    def __str__(self):
        return f"{self.title}"

class Step(models.Model):
    text = models.TextField(
        max_length=250, 
        verbose_name="Opis", help_text="Krok"
    )
    img = models.ImageField(
        upload_to="steps", 
        verbose_name="Obrázok", help_text="Pridajte obrazok ku kroku",
        blank=True, null=True, default=None
    )
    no = models.IntegerField(
        verbose_name="Krok cislo:", help_text="Zadaj poradie kroku"
    )
    
    date_modified = models.DateTimeField(auto_now=True, verbose_name="Naposledy upravené")

    # class Meta:
    #     # ensuring each recipe has only one unique step_no
    #     constraints = [
    #         models.UniqueConstraint(fields=['recipe','step_no'], name='unique_step_number')
    #     ]

    def __str__(self):
        return f"Krok č. {self.no}"

class Recipe(models.Model):
    title = models.CharField(max_length=63, unique=True, help_text="Názov receptu")
    description = models.TextField(max_length=127, verbose_name="Opis jedla", help_text="Zadajte stručný opis jedla")
    thumbnail = models.ImageField(
        upload_to="recipes", 
        help_text="Pridajte thumbnail", 
        blank=True, null=True, default=None)
    active = models.BooleanField(default=True, verbose_name="Aktívny")

    attributes = models.ManyToManyField(FoodAttribute, related_name="recipes", 
        blank=True
    )
    prep_time = models.IntegerField(
        verbose_name="Čas prípravy", help_text="Zadajte dĺžku prípravy"
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
    
    pescetarian = models.BooleanField(verbose_name="Pescetarian",default=False)
    vegetarian = models.BooleanField(verbose_name="Vegetarian",default=False)
    vegan = models.BooleanField(verbose_name="Vegan",default=False)
    gluten_free = models.BooleanField(verbose_name="Gluten Free",default=False)


    date_created = models.DateTimeField(auto_now_add=True, verbose_name="Čas vzniku")
    date_modified = models.DateTimeField(auto_now=True, verbose_name="Naposledy upravené")
    created_by = models.ForeignKey(User, related_name="recipes", 
        on_delete=models.SET_NULL,
        verbose_name="Created by", help_text="Zvolte seba",
        blank=True, null=True
    )

    def __str__(self):
        return f"{self.title}"

    def cost(self):
        # Needs attention
        pass

    def deactivate():
        # deactivates all of its verions
        pass

class RecipeOrderInstance(models.Model):
    recipe = models.ForeignKey('RecipeVersion',
        on_delete=models.CASCADE, related_name="order_instance")
    order = models.ForeignKey('home.Order',
        on_delete=models.CASCADE, related_name="order_instance")
    
    portions = models.IntegerField(
        verbose_name='Množstvo porcií'
    )

        # Rating
    choices_amount = [
        (None, "Vyhovovala vám porcia"),
        ("1", "Porcia bola malá"),
        ("2", "Porcia mohla byť trochu väčšia"), 
        ("3", "Porcia bola akurát"),
        ("4", "Stačilo by trochu menej"),
        ("5", "Porcia bola príliš veľká")]
    amount = models.CharField(
        blank=True, default=None, null=True, max_length=1,
        choices=choices_amount, 
        verbose_name="Hodnotenie množstva", help_text="Sedelo množstvo jedla s objednanou porciou?"
    )
    
    choices_stars = [("1", "1"), 
        ("2", "2"), 
        ("3", "3"), 
        ("4", "4"), 
        ("5", "5")]
    taste = models.CharField(
        blank=True, default=None, null=True, max_length=1,
        choices=choices_stars, 
        verbose_name="Chuť", help_text="Viac je lepšie"
    )
    delivery = models.CharField(
        blank=True, default=None, null=True, max_length=1,
        choices=choices_stars, 
        verbose_name="Doručenie", help_text="Viac je lepšie"
    )
    
class RecipeVersion(models.Model):
    recipe = models.ForeignKey(Recipe, related_name="versions",
        on_delete=models.PROTECT
    )
    version = models.IntegerField(
        verbose_name="Verzia receptu", help_text="Zadajte koľkatá je to verzia receptu"
    )
    
        # Actual recipe info 
    ingredients = models.ManyToManyField(Ingredient, through=IngredientInstance, related_name="recipes",
        help_text="Zvolte všetky ingrediencie"
    )
    steps = models.ManyToManyField(Step, related_name="recipes",
        blank=True, 
        verbose_name="Kroky", help_text="Pridajte kroky"
    )

    date_created = models.DateTimeField(auto_now_add=True, verbose_name="Čas vzniku")
    date_modified = models.DateTimeField(auto_now=True, verbose_name="Naposledy upravené")
    
    active = models.BooleanField(default=True, verbose_name="Aktívny")

    def __str__(self):
        return f"{self.recipe} v.{self.version}"

    # Returns a list of tuples, where first item is code and second title
    def get_alergens(self):
        alergens = set()
        for ingredient in self.ingredients.all():
            for alergen in ingredient.alergens.all():
                alergens.add((alergen.code, alergen.title))
        return list(alergens)

    def avg_rating(self):
        rating_sum = 0
        rating_num = 0
        for rating in self.order_instance.all():
            if rating.taste:
                rating_sum += int(rating.taste)
                rating_num += 1
        if rating_num:
            return rating_sum/rating_num
        return "No ratings"


class DeliveryDay(models.Model):

    date = models.DateField(blank=False, verbose_name="Dátum")

    recipes = models.ManyToManyField('recepty.RecipeVersion', related_name="delivery_days",
        verbose_name="Recepty na výber", help_text="Zvolte, ktoré recepty budú v daný deň na výber",
        blank=True
    )

    is_final = models.BooleanField(
        default=False, 
        help_text="If set to True, new orders will be created"
    )

    date_created = models.DateTimeField(auto_now_add=True, verbose_name="Čas vzniku")
    date_modified = models.DateTimeField(auto_now=True, verbose_name="Naposledy upravené")

    def save(self, *args, **kvargs):
        if self.is_final and self.date >= now().date():
            self.update_orders()
        return super().save(*args, **kvargs)


    def __str__(self):
        return f"Rozvoz z dňa {self.date}"

    def update_orders(self): # Create order for every active user
        # Localy import Object model
        Order = apps.get_model('home','Order')

        for user in User.objects.filter(is_active=True):
            user_alergies = set(user.profile.get_alergens())

            # Create order
            Order = apps.get_model('home','Order')
            order, created = Order.objects.update_or_create(user=user, delivery_day=self)

            # Get all recipes for a given user
            allowed_recipes = []
            for recipe in self.recipes.all():
                # If user vegan and recipe not
                if user.profile.vegan and not recipe.recipe.vegan: 
                    continue
                # If user vegetarian and recipe not
                elif user.profile.vegetarian and not (recipe.recipe.vegan or recipe.recipe.vegetarian):
                    continue
                # If user pescetarian and recipe not
                elif user.profile.pescetarian and not (recipe.recipe.vegan or recipe.recipe.vegetarian or recipe.recipe.pescetarian):
                    continue
                # If user gluten-free and recipe not
                elif user.profile.gluten_free and not recipe.recipe.gluten_free:
                    continue
                
                # If the food has any alergens user cant have
                food_alergies = set(recipe.get_alergens())
                if (user_alergies & food_alergies):
                    continue

                allowed_recipes.append(recipe)

            # Count matching attributes of each recipe with users preferences
            matching_attributes = {}
            for recipe in allowed_recipes:
                matching_attributes[recipe.id] = recipe.recipe.attributes.all().intersection(user.profile.food_preferences.all()).count()

            # Pick the recipes with the most matching cases
            recipes_w_portions = {}
            for i in range(constants.SELECTED_RECIPES_PER_DELIVERY_DAY): 
                if len(matching_attributes) == 0: # If no more foods are available
                    break
                recipes_w_portions[(max(matching_attributes, key=matching_attributes.get))] = user.profile.num_portions
                matching_attributes.pop(max(matching_attributes))
                
            # Add recipes to the Order
            for recipe in self.recipes.all():
                order.recipes.add(recipe, 
                    through_defaults = {'portions': recipes_w_portions.get(recipe.id, 0)}
                )
        

