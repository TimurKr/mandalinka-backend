# Generated by Django 4.1 on 2023-01-05 18:09

from django.db import migrations, models
import recipes.models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0027_remove_recipe_steps_step_step_step_number_uniqueness'),
    ]

    operations = [
        migrations.AlterField(
            model_name='step',
            name='number',
            field=models.IntegerField(validators=[recipes.models.validate_positivity], verbose_name='Poradie kroku'),
        ),
    ]