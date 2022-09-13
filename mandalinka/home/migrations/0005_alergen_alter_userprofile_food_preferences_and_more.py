# Generated by Django 4.1 on 2022-09-13 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_rename_food_attr_foodattribute'),
    ]

    operations = [
        migrations.CreateModel(
            name='Alergen',
            fields=[
                ('title', models.CharField(max_length=63, verbose_name='Alergén')),
                ('code', models.IntegerField(primary_key=True, serialize=False, verbose_name='Kód alergénu')),
            ],
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='food_preferences',
            field=models.ManyToManyField(related_name='users', to='home.foodattribute'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='alergies',
            field=models.ManyToManyField(related_name='users', to='home.alergen'),
        ),
    ]
