from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import MultipleObjectsReturned
from django.contrib.auth.backends import ModelBackend, UserModel
from django.db.models import Q

class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
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
        try:
            user = UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None

        return user if self.user_can_authenticate(user) else None


# Create your models here.

class UserProfile(models.Model):

    user_name = models.OneToOneField(User, related_name='profile', on_delete=models.DO_NOTHING)
    email = models.EmailField(max_length=254,blank=False)
    phone = models.CharField(max_length=20,blank=False)

    food_preferences = models.ManyToManyField(
        'recepty.FoodAttribute', 
        related_name="users",
        blank=True
    )
    alergies = models.ManyToManyField(
        'recepty.Alergen', 
        related_name="users", 
        blank=True
    )
    portions_options = [(2, "2"), (4, "4"), (6, "6")]
    num_portions = models.IntegerField(default=2, choices=portions_options, blank=False)

    street = models.CharField(max_length=150,blank=True)
    house_no = models.CharField(max_length=8, blank=False)
    district = models.CharField(max_length=50,blank=False)
    city = models.CharField(max_length=100,blank=False)
    postal = models.CharField(max_length=6,blank=False)
    country = models.CharField(max_length=16, blank=False)

    newsletter = models.BooleanField(default=False)
    terms_conditions = models.BooleanField(default=False)

    pescetarian = models.BooleanField(verbose_name="Pescetarian",default=False)
    vegetarian = models.BooleanField(verbose_name="Vegetarian",default=False)
    vegan = models.BooleanField(verbose_name="Vegan",default=False)
    gluten_free = models.BooleanField(verbose_name="Gluten Free",default=False)
    
    # def __unicode__(self):  # __str__
    #     return unicode(self.user_name)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user_name=instance)
        print("created")

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    # When you create a super user, it is imposible to log in to admin, this shows error.
    # comment the following line out, log in, edit your account fill in all requred fields,
    # and uncomment it again
    instance.profile.save()
    print("saved")

User._meta.get_field('email')._unique = True

class Streets(models.Model):
    street = models.CharField(max_length=150)

class CityDistrictPostal(models.Model):
    city = models.CharField(max_length=150)
    street = models.CharField(max_length=100)
    district = models.CharField(max_length=150)
    postal = models.CharField(max_length=150)
    country = models.CharField(blank=False, max_length=3)

    

class Order(models.Model):
    # If user is null, his/her account has been deleted
    user = models.ForeignKey(User, related_name='orders', 
        on_delete=models.SET_NULL, null=True
    )
    delivery_day = models.ForeignKey('recepty.DeliveryDay', related_name='orders', 
        on_delete=models.SET_NULL, null=True,
    )
    recipes = models.ManyToManyField('recepty.RecipeVersion', through='recepty.RecipeOrderInstance', related_name='orders',
        blank=True,
        verbose_name='Recepty', help_text='Zvolte si recepty a množstvo porcií'
    )
