# Generated by Django 4.1 on 2022-09-04 18:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Alergen',
            fields=[
                ('title', models.CharField(max_length=63, verbose_name='Alergén')),
                ('code', models.IntegerField(primary_key=True, serialize=False, verbose_name='Kód alergénu')),
            ],
        ),
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Názov ingrediencie', max_length=31, unique=True, verbose_name='Názov')),
                ('price_per_unit', models.FloatField(help_text='Zadajte cenu na nižšie zvolenú jednotku', verbose_name='Cena na jednotku')),
                ('unit', models.CharField(choices=[('', 'Zvolte jednotku'), ('g', 'gramy'), ('ml', 'mililitre')], help_text='Zvolte jednotku', max_length=3, verbose_name='Jednotka')),
                ('alergens', models.ManyToManyField(blank=True, help_text='Zvolte všetky alergény:', related_name='Ingredients', to='recepty.alergen', verbose_name='Alergény')),
            ],
        ),
        migrations.CreateModel(
            name='IngredientInstance',
            fields=[
                ('amount', models.IntegerField(help_text='Zadajte množstvo danej potraviny', primary_key=True, serialize=False, verbose_name='Množstvo')),
                ('ingredient', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='recepty.ingredient')),
            ],
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Názov receptu', max_length=63, unique=True)),
                ('description', models.TextField(help_text='Zadajte stručný opis jedla', max_length=127, verbose_name='Opis jedla')),
                ('prep_time', models.IntegerField(help_text='Zadajte dĺžku prípravy', verbose_name='Čas prípravy')),
                ('thumbnail', models.ImageField(default=None, help_text='Pridajte thumbnail', upload_to='recepty/static/photos/')),
                ('ingredients', models.ManyToManyField(help_text='Zvolte všetky ingrediencie', related_name='Recipes', through='recepty.IngredientInstance', to='recepty.ingredient')),
            ],
        ),
        migrations.AddField(
            model_name='ingredientinstance',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recepty.recipe'),
        ),
    ]