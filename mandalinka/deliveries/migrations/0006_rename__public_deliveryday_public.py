# Generated by Django 4.1 on 2023-01-03 15:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('deliveries', '0005_alter_deliveryday__public'),
    ]

    operations = [
        migrations.RenameField(
            model_name='deliveryday',
            old_name='_public',
            new_name='public',
        ),
    ]
