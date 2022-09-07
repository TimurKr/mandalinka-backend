# Generated by Django 4.1 on 2022-09-07 11:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recepty', '0023_remove_rating_recipe'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rating',
            name='recipe_instance',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ratings', to='recepty.recipeinstance'),
        ),
    ]