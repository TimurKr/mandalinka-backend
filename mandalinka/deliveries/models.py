from django.db import models

# Create your models here.


class DeliveryDay(models.Model):
    date = models.DateField(verbose_name='Dátum', 
        blank=False, unique=True
    )
    recipes = models.ManyToManyField('recipes.Recipe', through='recipes.RecipeDeliveryInstance' ,related_name='delivery_days',
        verbose_name='Recepty', help_text="Zvolte, ktoré recepty budú v daný deň na výber",
        blank=True
    )

    date_created = models.DateTimeField(auto_now_add=True, verbose_name="Čas vzniku")
    date_modified = models.DateTimeField(auto_now=True, verbose_name="Naposledy upravené")

    def __str__(self):
        return f"Objednávka z dňa {self.date.strftime('%d.%m.%Y')}"

    def save(self, generate_orders: bool = False, *args, **kwargs):
        super().save(*args, **kwargs)
        if generate_orders: 
            # generate orders
            pass