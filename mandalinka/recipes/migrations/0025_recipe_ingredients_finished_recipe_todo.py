# Generated by Django 4.1 on 2023-01-05 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0024_alter_recipe_thumbnail'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='ingredients_finished',
            field=models.BooleanField(default=False, help_text='Odznačte, ak ešte treba ingrediencie prerobiť/opraviť', verbose_name='Ingrediencie finálne hotové'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='todo',
            field=models.TextField(blank=True, help_text='Sem napíš všetko, čo ešte pre tento recept nie je hotové. Veci oddeluj enterom.', verbose_name='ToDo poznámka'),
        ),
    ]
