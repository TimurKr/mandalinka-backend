# Generated by Django 4.1 on 2023-01-05 18:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0028_alter_step_number'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='step',
            name='step_number_uniqueness',
        ),
    ]
