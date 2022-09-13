from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.
class FoodAttribute(models.Model):
    attr = models.CharField(max_length=255)

    def __str__(self):
        return self.attr

class UserProfile(models.Model):

    user_name = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    email = models.EmailField(max_length=254,blank=False)
    phone = models.CharField(max_length=20,blank=False)

    food_preferences = models.ManyToManyField(FoodAttribute)

    street = models.CharField(max_length=150,blank=True)
    house_no = models.CharField(max_length=8, blank=False)
    district = models.CharField(max_length=50,blank=False)
    city = models.CharField(max_length=100,blank=False)
    postal = models.CharField(max_length=5,blank=False)
    country = models.CharField(max_length=2, blank=False)

    newsletter = models.BooleanField(default=False)
    terms_conditions = models.BooleanField(default=False)
    
    def __unicode__(self):  # __str__
        return unicode(self.user_name)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user_name=instance)
        print("created")

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
    print("saved")

User._meta.get_field('email')._unique = True

class Districts(models.Model):
    district = models.CharField(max_length=40)

class Cities(models.Model):
    city = models.CharField(max_length=100)

class PostalCodes(models.Model):
    code = models.CharField(max_length=5)

class Streets(models.Model):
    street = models.CharField(max_length=150)

class CityDistrictPostal(models.Model):
    city = models.CharField(max_length=150)
    district = models.CharField(max_length=150)
    postal = models.CharField(max_length=150)
    country = models.CharField(blank=False, max_length=3)
