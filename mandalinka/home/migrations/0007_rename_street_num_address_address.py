# Generated by Django 4.1 on 2022-10-22 12:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_alter_user_addresses'),
    ]

    operations = [
        migrations.RenameField(
            model_name='address',
            old_name='street_num',
            new_name='address',
        ),
    ]