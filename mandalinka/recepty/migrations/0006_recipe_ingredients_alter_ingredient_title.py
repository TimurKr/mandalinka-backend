# Generated by Django 4.1 on 2022-09-04 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recepty', '0005_alter_ingredient_price_per_unit_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='ingredients',
            field=models.ManyToManyField(help_text='Zvolte všetky ingrediencie', to='recepty.ingredient'),
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='title',
            field=models.CharField(help_text='Názov ingrediencie', max_length=31, unique=True, verbose_name='Názov'),
        ),
    ]
