# Generated by Django 4.1 on 2022-09-07 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recepty', '0011_recipeinstance_date_created_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipeversion',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, default=None, verbose_name='Čas vzniku'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='recipeversion',
            name='date_modified',
            field=models.DateTimeField(auto_now=True, verbose_name='Naposledy upravené'),
        ),
    ]
