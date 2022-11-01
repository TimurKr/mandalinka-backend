# To inherit models
from re import I
from django.db import models
from django.contrib.auth.models import AbstractUser

# To recieve signals
from django.dispatch import receiver


#################### Users #######################

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
    food_preferences = models.ManyToManyField('recipes.Attribute', 
        related_name="users",
        blank=True
    )
    alergies = models.ManyToManyField('recipes.Alergen', 
        related_name="users", 
        blank=True
    )
    diet = models.ManyToManyField('recipes.Diet', 
        related_name='users'
    )


    class Meta(AbstractUser.Meta):
        abstract = False

    def __str__(self):
        return self.get_full_name()


    # def get_alergens(self):
    #     alergens = set()
    #     for alergen in self.alergies.all():
    #         alergens.add((alergen.code, alergen.title))
    #     return list(alergens)


    # def add_address(self, address: Address):
    #     if address.primary:
    #         for a in self.addresses.all():
    #             a.primary = False
    #             a.save()
    #     self.addresses.add(address)
    #     self.save()

@receiver(models.signals.pre_save, sender=User)
def create_user_profile(sender, instance, created=False, **kwargs):
    if created and not instance.username:
        instance.username = instance.get_full_name()

# Email verification 
# to be able to verify through email as well as password

from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.core.exceptions import MultipleObjectsReturned
class EmailVerification(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        try: #to allow authentication through phone number or any other field, modify the below statement
            user = UserModel.objects.get(models.Q(username__iexact=username) | models.Q(email__iexact=username))
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


#################### Addresses #######################

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

    user = models.ForeignKey('accounts.User', blank=True, null=True, related_name='addresses', on_delete=models.CASCADE)

    def __str__(self):
        if self.primary:
            return '*%s*: %s' % (self.name, self.address)
        return '%s: %s' % (self.name, self.address)

    def make_primary(self):
        self.primary = True
        self.save()

@receiver(models.signals.post_delete, sender=Address)
def choose_new_primary_address(sender, instance, using, **kwargs):
    """ Prevent from not having primary address"""
    if not instance.primary: return
    user = instance.user
    if not user: return
    addresses = user.addresses.all()
    if addresses.count() == 0:
        # Send notification once notifications are implemented
        pass
    addresses.first().make_primary()

@receiver(models.signals.post_save, sender=Address)
def pick_primary_address(sender, instance, using, **kwargs):
    """ Prevent form existing 2 primary addressess"""
    if not instance.primary: return
    user = instance.user
    if not user: return
    prev_primary_address = user.addresses.exclude(pk=instance.pk).filter(primary=True)
    if prev_primary_address.count() == 0: return
    prev_primary_address = prev_primary_address.first()
    prev_primary_address.primary = False
    prev_primary_address.save()
    

