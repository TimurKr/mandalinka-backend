# Generated by Django 4.1 on 2022-09-25 10:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_order_delivery_day_alter_order_recipes_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='country',
            field=models.CharField(max_length=16),
        ),
    ]
