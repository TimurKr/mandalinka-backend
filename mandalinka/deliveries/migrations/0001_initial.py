# Generated by Django 4.1 on 2022-11-05 13:13

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DeliveryDay',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(unique=True, verbose_name='Dátum')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Čas vzniku')),
                ('date_modified', models.DateTimeField(auto_now=True, verbose_name='Naposledy upravené')),
            ],
        ),
    ]