# Generated by Django 4.1 on 2022-10-25 17:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0004_ingredientinstance_recipe_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='attributes',
            field=models.ManyToManyField(blank=True, related_name='recipes', to='recipes.attribute'),
        ),
    ]
