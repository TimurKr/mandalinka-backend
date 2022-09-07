# Generated by Django 4.1 on 2022-09-06 11:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recepty', '0004_alter_step_recipe'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipe',
            name='ingredients',
        ),
        migrations.RemoveField(
            model_name='recipe',
            name='prep_time',
        ),
        migrations.RemoveField(
            model_name='recipe',
            name='steps',
        ),
        migrations.CreateModel(
            name='RecipeVersion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('version', models.IntegerField(help_text='Zadajte koľkatá je to verzia receptu', verbose_name='Verzia receptu')),
                ('prep_time', models.IntegerField(help_text='Zadajte dĺžku prípravy', verbose_name='Čas prípravy')),
                ('ingredients', models.ManyToManyField(help_text='Zvolte všetky ingrediencie', related_name='recipes', through='recepty.IngredientInstance', to='recepty.ingredient')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipe_versions', to='recepty.recipe')),
                ('steps', models.ManyToManyField(help_text='Pridajte kroky', related_name='recipes', to='recepty.step')),
            ],
        ),
        migrations.AlterField(
            model_name='ingredientinstance',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recepty.recipeversion'),
        ),
        migrations.AlterField(
            model_name='step',
            name='recipe',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Recipes', to='recepty.recipeversion'),
        ),
    ]