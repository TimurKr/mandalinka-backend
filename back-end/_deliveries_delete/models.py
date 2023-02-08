from django.db import models

from utils.models import TimeStampedMixin

# Create your models here.

class DeliveryDay(TimeStampedMixin, models.Model):
    date = models.DateField(verbose_name='Dátum', 
        blank=False, unique=True
    )

    public= models.BooleanField(default=False,
        help_text='Označuje, či je recept verejný. '
            'Nikde nemeniť manuálne, iba pomocou save(public=True)',
        editable=False,
    )


    class Meta:
        pass

    def __str__(self):
        return f"Objednávka z dňa {self.date.strftime('%d.%m.%Y')}"


    def save(self, public: bool = False, *args, **kwargs):
        """
        Saves the object and generates all future orders for all users

        public: bool -> True makes public true and generates orders for all users
        """
        if public and not self._public:
            self._public
            super().save(*args, **kwargs)
            self.generate_orders()
        else:
            super().save(*args, **kwargs)


    def generate_orders(self):
        """
        Generate an order for all active users
        If the order has been created and the user is subscribed, automaticaly order best recipes
        """
        from django.apps import apps    
        User = apps.get_model('accounts', 'User')

        for user in User.objects.filter(is_active=True):
            (order, created) = user.orders.get_or_create(delivery_day=self)
            if created and user.is_subscribed: 
                order.automaticaly_generate()

