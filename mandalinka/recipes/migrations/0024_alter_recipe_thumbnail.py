# Generated by Django 4.1 on 2023-01-04 19:50

from django.db import migrations, models
import recipes.models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0023_remove_recipe_errors_recipe_automatic_errors_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='thumbnail',
            field=models.ImageField(blank=True, help_text='Pridajte thumbnail', null=True, upload_to=recipes.models.Recipe.thumbnail_upload_to),
        ),
    ]
