# To inherit models
from email.policy import default
from re import I
from django.db import models
from django.db.models import Q
from django.contrib.auth.models import AbstractUser
from recipes.models import Diet

# To recieve signals
from django.dispatch import receiver

# To handle exceptions
from django.core.exceptions import ObjectDoesNotExist, ValidationError

import datetime

#################### Addresses #######################

class Address(models.Model):
    name = models.CharField(max_length=32, default="Domov", verbose_name="Názov adresy")
    address = models.CharField(max_length=128, verbose_name="Adresa a číslo domu", help_text="Nezabudnite pridať číslo domu")
    note = models.TextField(max_length=256, blank=True, verbose_name="Poznámka pre kuriéra", help_text="(zvonček, poschodie, ...)")
    city = models.CharField(max_length=100, verbose_name="Mesto")
    district = models.CharField(max_length=50,blank=True, verbose_name="Okres")
    postal = models.CharField(max_length=6, verbose_name="PSČ")
    country = models.CharField(max_length=32, blank=True, verbose_name="Krajina")
    coordinates = models.CharField(max_length=64)

    primary = models.BooleanField(default=True)

    user = models.ForeignKey('accounts.User', related_name='addresses', on_delete=models.CASCADE)

    def __str__(self):
        if self.primary:
            return '*%s*: %s' % (self.name, self.address)
        return '%s: %s' % (self.name, self.address)

    def make_primary(self):
        if self.primary: return
        self.primary = True
        self.save()

@receiver(models.signals.post_delete, sender=Address)
def choose_new_primary_address(sender, instance, using, **kwargs):
    """ Prevent from not having primary address"""
    if not instance.primary: return
    try:
        user = instance.user
    except ObjectDoesNotExist:
        return
    if not user: return
    addresses = user.addresses.all()
    if addresses.count() == 0:
        # TODO: Send notification once notifications are implemented
        return
    addresses.last().make_primary()

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
    


#################### Users #######################
def default_diet():
    return Diet.objects.get(name='Bez diety')

class User(AbstractUser):
    # Basics
    first_name = models.CharField('Meno', max_length=150)
    last_name = models.CharField('Priezvisko', max_length=150)
    PRONOUNS = (
        ('male', 'Mužský rod'),
        ('female', 'Ženský rod'),
    )
    pronoun = models.CharField('Oslovovanie', max_length=16, choices=PRONOUNS)
    email = models.EmailField('Email', unique=True)
    phone = models.CharField('Telefónne číslo', help_text='Môže byť použité počas doručovania', max_length=20, default='+421')
    newsletter = models.BooleanField(default=True)
    terms_conditions = models.BooleanField(blank=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username','first_name', 'last_name', 'phone', 'terms_conditions')

    # Validations
    is_active = models.BooleanField(default=True,
        help_text=
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
    )
    _is_email_valid = models.BooleanField(default=False, 
        help_text=
            "Designates whether this user has confirmed email. "
    )
    _is_payment_valid = models.BooleanField(default=False, 
        help_text=
            "Designates whether this user has a valid payment option. "
    )
    _is_subscribed = models.BooleanField(default=False,
        help_text=
            "Designates whether this user is subscribed, has automatic payments turned on. "
    )

    # Preferences
    default_num_portions = models.IntegerField(
        default=4, blank=False, choices=((2,2),(4,4),(6,6)),
        verbose_name='Počet porcií', help_text='Koľko vás bude pravidelne jedávať?')
    default_pickup = models.BooleanField(default=False,
        verbose_name='Osobné vyzdvihovanie', help_text='Zaškrtnite, ak si želáte objednávky vyzdvihovať osobne u nás v kamennej predajni.'
    )
    food_preferences = models.ManyToManyField('recipes.Attribute', related_name="users",
        blank=True, 
        verbose_name='Preferencie', help_text='Pri zvolení automatického objednávania vám vyberieme jedlá, ktoré budú zdielať najviac atríbutov s vašimi preferenciami.',
    )
    alergies = models.ManyToManyField('recipes.Alergen', related_name="users", 
        blank=True, default=None,
        verbose_name='Alergie', help_text="Máte nejaké alergie? Povedzte nám o nich teraz a my vám nikdy automaticky neobjednáme recept obsahujúci daný alergén."
    )
    diet = models.ManyToManyField('recipes.Diet', related_name='users',
        blank=True, default=None,
        verbose_name='Diety', help_text='Máte nejaké diety? Pri automatickom objednávanií vám budeme vyberať iba z jednál, ktoré spadajú do vašej diety.',
    )


    class Meta(AbstractUser.Meta):
        abstract = False

        constraints = [
            models.CheckConstraint(
                check=Q(_is_subscribed=True, _is_payment_valid=True) | Q(_is_subscribed=False),
                name='Payment is required for subscription'),
            models.CheckConstraint(
                check=Q(_is_payment_valid=True, _is_email_valid=True) | Q(_is_payment_valid=False),
                name='Email confirmation is required for adding payment method'),
            models.CheckConstraint(
                check=Q(_is_subscribed=True, is_active=True) | Q(_is_subscribed=False),
                name='Being active is required for subscription'),
        ]


    ### OUTPUTS ###
    def __str__(self):
        return self.get_full_name()

    def get_alergens(self):
        """Return a set of alergies in the format ((code, name), (code, name), ...)"""
        alergens = set()
        for alergen in self.alergies.all():
            alergens.add((alergen.code, alergen.name))
        return list(alergens)


    ### INPUTS ###
    def deactivate_account(self):
        self.is_subscribed = False
        self.is_payment_valid = False
        self.is_email_valid = False
        self.is_active = False
        self.__delete_all_future_orders()

    def validate_email(self):
        self.is_email_valid = True
        self.__generate_empty_orders()
        self.save()

    def validate_payment(self):
        self.is_payment_valid = True
        self.save()

    def start_subscription(self, force: bool = False):
        """
        Subscribtion generates all new orders
        force: bool -> True overrides the need for valid payment, doesn't make _is_subscribed True
        """
        try:
            print('Trying to turn on subscription...')
            self._is_subscribed = True
            self.save()
        except Exception as e:
            print('Failed to turn on subscription')
            if not force:
                print('Raising error:')
                raise e
        finally:
            print('Force made me continue...')
            self.__populate_future_orders(force=force)
            # TODO: send success notification

    ### METHODS ###
    def __generate_empty_orders(self): # When new user is created
        from django.apps import apps    
        DeliveryDay = apps.get_model('deliveries', 'DeliveryDay')
        for delivery_day in DeliveryDay.objects.filter(date__gte=datetime.date.today(), public=True):
            self.orders.get_or_create(delivery_day=delivery_day)

    def __delete_all_future_orders(self):
        self.order.filter(delivery_day__date__gte=datetime.date.today(), payed=False).delete()
    
    def populate_next_order(self):
        """This relies on the fact that there is at least one future order"""
        self.orders.filter(delivery_day__date__gte=datetime.date.today()).order_by('date').first().automaticaly_generate()


    def __populate_future_orders(self, force=False):
        """This relies on the fact that all future empty orders were created"""
        for order in self.orders.filter(delivery_day__date__gte=datetime.date.today()):
            order.automaticaly_generate(force=force)




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

