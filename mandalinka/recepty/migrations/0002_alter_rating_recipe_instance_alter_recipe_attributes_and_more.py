# Generated by Django 4.1 on 2022-09-18 15:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recepty', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rating',
            name='recipe_instance',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ratings', to='recepty.recipeversion'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='attributes',
            field=models.ManyToManyField(blank=True, related_name='recipes', to='recepty.foodattribute'),
        ),
        migrations.DeleteModel(
            name='RecipeInstance',
        ),
    ]