# Generated by Django 4.1 on 2022-11-01 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='diet',
            name='name',
            field=models.CharField(max_length=32, primary_key=True, serialize=False),
        ),
    ]
