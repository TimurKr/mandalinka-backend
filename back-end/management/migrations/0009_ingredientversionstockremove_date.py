# Generated by Django 4.1 on 2023-03-16 14:18

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0008_alter_ingredientversionstockchange_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='ingredientversionstockremove',
            name='date',
            field=models.DateTimeField(default=datetime.datetime.now, help_text='Zadajte dátum odobratia', verbose_name='Dátum'),
        ),
    ]
