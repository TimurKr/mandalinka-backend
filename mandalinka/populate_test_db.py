from psycopg2.errors import UniqueViolation
import datetime

from accounts.models import User
from recipes import models as recipe_models
from customers import models as customers_models
from deliveries import models as deliveries_models

class Error(Exception):
    pass

def run():
    print('Running...')

    # Alergens
    recipe_models.Alergen.objects.get_or_create(name='Lepok', code='1')
    recipe_models.Alergen.objects.get_or_create(name='Vajcia', code='3')
    recipe_models.Alergen.objects.get_or_create(name='Mliečne výrobky', code='7')

    # Attributes
    recipe_models.Attribute.objects.get_or_create(name='Pizza')
    recipe_models.Attribute.objects.get_or_create(name='Asian')
    recipe_models.Attribute.objects.get_or_create(name='Pasta')
    recipe_models.Attribute.objects.get_or_create(name='Sea-Food')

    # Diets
    recipe_models.Diet.objects.get_or_create(name='Vegan')
    recipe_models.Diet.objects.get_or_create(name='Vegetarian')
    recipe_models.Diet.objects.get_or_create(name='Pescetarian')


    # Ingredients
    (ryža, created) = recipe_models.Ingredient.objects.get_or_create(
        name='Ryža',
        unit='g',
        price_per_unit=0.002,
    )
    (vajce, created) = recipe_models.Ingredient.objects.get_or_create(
        name='Vajce',
        unit='ks',
        price_per_unit=0.24,
    )
    vajce.alergens.add(recipe_models.Alergen.objects.get(code='3'))


    # Recipes
    (r1, created) = recipe_models.Recipe.objects.get_or_create(
        name='Ryža s vajcom', 
        description='Skvelé low-cost jedlo',
        is_active=True,
        steps='Uvar ryžu\nDaj ryžu na panvicu\nDo horúcej ryže vhoď vajíčko\nVar kým nedosiahne ksvelú konzistenciu', 
        difficulty=1,
        StF_time=30, active_time=10,
        created_by=User.objects.filter(is_superuser=True).first()
    )
    r1.attributes.set(recipe_models.Attribute.objects.filter(name='Asian'))
    r1.diet.set(recipe_models.Diet.objects.filter(name='Vegetarian'))
    r1.ingredients.clear()
    r1.ingredients.add(ryža, through_defaults={'amount': 100})
    r1.ingredients.add(vajce, through_defaults={'amount': 1})


    # DeliveryDays
    (dd1, created) = deliveries_models.DeliveryDay.objects.get_or_create(
        date=datetime.date(2023, 12, 5)
    )
    dd1.recipes.clear()
    dd1.recipes.add(r1)


    # Orders
    (o1, created) = customers_models.Order.objects.get_or_create(
        user=User.objects.filter(is_superuser=True).first(),
        delivery_day=dd1,
    )
    o1.recipes.clear()
    o1.recipes.add(r1, through_defaults={'portions': 4})



    print('All created')