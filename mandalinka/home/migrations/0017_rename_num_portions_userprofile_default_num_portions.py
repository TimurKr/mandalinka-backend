# Generated by Django 4.1 on 2022-10-19 08:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0016_userprofile_is_address_valid_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='num_portions',
            new_name='default_num_portions',
        ),
    ]
