# Generated by Django 4.1 on 2022-09-05 15:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recepty', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredient',
            name='unit',
            field=models.CharField(choices=[('', 'Zvolte jednotku'), ('g', 'gramy'), ('ml', 'mililitre'), ('ks', 'kusy')], help_text='Zvolte jednotku', max_length=3, verbose_name='Jednotka'),
        ),
        migrations.AlterField(
            model_name='step',
            name='recipe',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='Recipes', to='recepty.recipe'),
        ),
    ]