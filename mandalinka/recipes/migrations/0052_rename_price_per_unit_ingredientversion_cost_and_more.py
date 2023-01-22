# Generated by Django 4.1 on 2023-01-18 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0051_ingredientinrecipe_alter_recipe_ingredients_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ingredientversion',
            old_name='price_per_unit',
            new_name='cost',
        ),
        migrations.AlterField(
            model_name='ingredientversion',
            name='status',
            field=models.CharField(choices=[('Preparation', 'Preparation'), ('Active', 'Active'), ('Retired', 'Retired')], default='Preparation', editable=False, max_length=20),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='status',
            field=models.CharField(choices=[('Preparation', 'Preparation'), ('Active', 'Active'), ('Retired', 'Retired')], default='Preparation', editable=False, max_length=20),
        ),
    ]