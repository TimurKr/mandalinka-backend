# Generated by Django 4.1 on 2022-10-25 17:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_attribute_rename_title_alergen_name_and_more'),
        ('accounts', '0004_user_diets'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='alergies',
            field=models.ManyToManyField(blank=True, related_name='users', to='recipes.alergen'),
        ),
        migrations.AddField(
            model_name='user',
            name='food_preferences',
            field=models.ManyToManyField(blank=True, related_name='users', to='recipes.attribute'),
        ),
    ]
