# Generated by Django 4.1 on 2022-12-19 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0014_alter_recipe_ingredients'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredient',
            name='price_per_unit',
            field=models.FloatField(help_text='Zadajte cenu na zvolenú jednotku', verbose_name='Cena na jednotku'),
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='unit',
            field=models.CharField(choices=[(None, 'Zvolte jednotku'), ('g', 'Gram'), ('ml', 'Mililiter'), ('ks', 'Kus')], help_text='Zvolte jednotku', max_length=3, verbose_name='Jednotka'),
        ),
    ]