# Generated by Django 4.1 on 2022-09-05 15:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recepty', '0003_alter_step_recipe'),
    ]

    operations = [
        migrations.AlterField(
            model_name='step',
            name='recipe',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Recipes', to='recepty.recipe'),
        ),
    ]
