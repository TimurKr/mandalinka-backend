# Generated by Django 4.1 on 2022-11-20 12:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0013_alter_ingredient_options_alter_recipe_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='ingredients',
            field=models.ManyToManyField(blank=True, help_text='Zvolte všetky ingrediencie', related_name='recipes', through='recipes.IngredientInstance', to='recipes.ingredient', verbose_name='Ingrediencie'),
        ),
    ]