# Generated by Django 4.1 on 2022-10-19 08:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0015_alter_userprofile_user_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='is_address_valid',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='is_email_valid',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='is_payment_valid',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='is_subscribed',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='num_portions',
            field=models.IntegerField(default=2),
        ),
    ]
