# Generated by Django 4.1 on 2023-01-10 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0033_recipe_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='Statuses',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.RemoveField(
            model_name='recipe',
            name='is_active',
        ),
        migrations.AlterField(
            model_name='recipe',
            name='status',
            field=models.CharField(choices=[('Preparation', 'Preparation'), ('Active', 'Active'), ('Retired', 'Retired')], default='Active', max_length=20),
        ),
    ]
