# Generated by Django 4.1 on 2023-01-22 13:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0056_recipeerror_remove_ingredient_alergens_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='recipeerror',
            options={'ordering': ['code']},
        ),
        migrations.RenameField(
            model_name='recipe',
            old_name='automatic_errors',
            new_name='_automatic_errors',
        ),
    ]
