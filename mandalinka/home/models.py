from __future__ import unicode_literals
from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.core.exceptions import MultipleObjectsReturned
from django.db.models import Q
from django.apps import apps
from mandalinka import constants




# Create your models here.
class Address(models.Model):
    name = models.CharField(max_length=32, default="Domov", verbose_name="Názov adresy", help_text="Názov, pod ktorým uložíme túto adresu")
    address = models.CharField(max_length=128, verbose_name="Adresa a číslo domu", help_text="Nezabudnite pridať číslo domu")
    note = models.TextField(max_length=256, blank=True, verbose_name="Poznámka pre kuriéra", help_text="(zvonček, poschodie, ...)")
    city = models.CharField(max_length=100, verbose_name="Mesto")
    district = models.CharField(max_length=50,blank=True, verbose_name="Okres")
    postal = models.CharField(max_length=6, verbose_name="PSČ")
    country = models.CharField(max_length=32, blank=True, verbose_name="Krajina")
    coordinates = models.CharField(max_length=64)

    primary = models.BooleanField(default=True)

    user = models.ForeignKey('home.User', blank=True, null=True, related_name='addresses', on_delete=models.CASCADE)

    def __str__(self):
        return '%s: %s' % (self.name, self.address)

    def set_primary(self):
        prev_primary = self.user.addresses.get(primary=True)
        prev_primary.primary = False
        prev_primary.save()
        self.primary = True
        self.save()

class Diet(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name

class User(AbstractUser):

    # Basics
    first_name = models.CharField('Meno', max_length=150)
    last_name = models.CharField('Priezvisko', max_length=150)
    PRONOUNS = (
        ('male', 'Mužský rod'),
        ('female', 'Ženský rod'),
        ('they', 'Vykanie'),
    )
    pronoun = models.CharField('Oslovovanie', max_length=16, choices=PRONOUNS)
    email = models.EmailField('Email', unique=True)
    phone = models.CharField('Telefónne číslo', help_text='Môže byť použité počas doručovania', max_length=20, default='+421')
    newsletter = models.BooleanField(default=True)
    terms_conditions = models.BooleanField(blank=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('first_name', 'last_name', 'phone', 'terms_conditions')

    # Validations
    is_email_valid = models.BooleanField(default=False)
    is_payment_valid = models.BooleanField(default=False)
    is_subscribed = models.BooleanField(default=False)

    # Preferences
    default_num_portions = models.IntegerField(default=4, blank=False, choices=((2,2),(4,4),(6,6)))
    food_preferences = models.ManyToManyField('recepty.FoodAttribute', 
        related_name="users",
        blank=True
    )
    alergies = models.ManyToManyField('recepty.Alergen', 
        related_name="users", 
        blank=True
    )
    diets = models.ManyToManyField(Diet, 
        related_name='users',
        blank=True)

    # pescetarian = models.BooleanField(verbose_name="Pescetarian",default=False)
    # vegetarian = models.BooleanField(verbose_name="Vegetarian",default=False)
    # vegan = models.BooleanField(verbose_name="Vegan",default=False)
    # gluten_free = models.BooleanField(verbose_name="Gluten Free",default=False)

    class Meta(AbstractUser.Meta):
        abstract = False

    def get_alergens(self):
        alergens = set()
        for alergen in self.alergies.all():
            alergens.add((alergen.code, alergen.title))
        return list(alergens)

    def generate_future_orders(self):
        """ This function is called after activation, 
        creates Orders for all future delivery_days """
        pass

    def add_address(self, address: Address):
        if address.primary:
            for a in self.addresses.all():
                a.primary = False
                a.save()
        self.addresses.add(address)
        self.save()
    
    
@receiver(post_delete, sender=Address)
def choose_new_primary_address(sender, instance, using, **kwargs):
    if instance.primary:
        try:
            user = instance.user
        except:
            return
        if user is None:
            return
        try:
            address = user.addresses.first()
        except:
            return
        address.primary = True
        address.save()


# To sign in either with username or with email

from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
class EmailVerification(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        try: #to allow authentication through phone number or any other field, modify the below statement
            user = UserModel.objects.get(Q(username__iexact=username) | Q(email__iexact=username))
        except UserModel.DoesNotExist:
            UserModel().set_password(password)
        except MultipleObjectsReturned:
            return User.objects.filter(email=username).order_by('id').first()
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user

    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None

        return user if self.user_can_authenticate(user) else None


# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         UserProfile.objects.create(user_name=instance)
#         print("created")

# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     # When you create a super user, it is imposible to log in to admin, this shows error.
#     # comment the following line out, log in, edit your account fill in all requred fields,
#     # and uncomment it again
#     instance.profile.save()
#     print("saved")

# User._meta.get_field('email')._unique = True


class Order(models.Model):
    # If user is null, his/her account has been deleted
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='orders', 
        on_delete=models.PROTECT, null=True
    )
    delivery_day = models.ForeignKey('recepty.DeliveryDay', related_name='orders', 
        on_delete=models.PROTECT, null=True,
    )

    recipes = models.ManyToManyField('recepty.RecipeVersion', through='recepty.RecipeOrderInstance', related_name='orders',
        blank=True,
        verbose_name='Recepty', help_text='Zvolte si recepty a množstvo porcií'
    )

    pickup = models.BooleanField(default=False)

    def get_portions(self):
        """ Returns the total number of portions """
        sum = 0
        for recipe in self.order_instance.all():
            sum += recipe.portions
        return sum

    def is_fullfilled(self):
        """ Returns False if not enough portions is ordered """
        portions = self.get_portions()
        required_portions = self.user.profile.num_portions * constants.SELECTED_RECIPES_PER_DELIVERY_DAY
        if portions < required_portions:
            return False
        return True

    def toggle_pickup(self):
        if self.pickup:
            self.pickup = False
        else:
            self.pickup = True
        self.save()
        


