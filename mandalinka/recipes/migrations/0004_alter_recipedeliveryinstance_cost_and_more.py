# Generated by Django 4.1 on 2022-11-05 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0003_alter_ingredient_alergens'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipedeliveryinstance',
            name='cost',
            field=models.FloatField(blank=True, default=None, verbose_name='Reálne náklady'),
        ),
        migrations.AlterField(
            model_name='recipedeliveryinstance',
            name='price',
            field=models.FloatField(blank=True, default=None, verbose_name='Predajná cena'),
        ),
    ]