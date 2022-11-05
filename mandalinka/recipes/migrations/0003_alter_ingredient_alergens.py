# Generated by Django 4.1 on 2022-11-05 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_rename_active_recipe_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredient',
            name='alergens',
            field=models.ManyToManyField(blank=True, default=None, help_text='Zvolte všetky alergény:', related_name='ingredients', to='recipes.alergen', verbose_name='Alergény'),
        ),
    ]
