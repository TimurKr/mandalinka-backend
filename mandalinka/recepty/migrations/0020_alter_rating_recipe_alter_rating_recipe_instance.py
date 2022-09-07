# Generated by Django 4.1 on 2022-09-07 11:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recepty', '0019_rating_recipe_alter_rating_amount_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rating',
            name='recipe',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='ratings', to='recepty.recipe'),
        ),
        migrations.AlterField(
            model_name='rating',
            name='recipe_instance',
            field=models.ForeignKey(limit_choices_to={'recipe_version.recipe': models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='ratings', to='recepty.recipe')}, on_delete=django.db.models.deletion.CASCADE, related_name='ratings', to='recepty.recipeinstance'),
        ),
    ]
