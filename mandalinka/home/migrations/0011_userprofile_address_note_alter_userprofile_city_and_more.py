# Generated by Django 4.1 on 2022-10-16 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0010_remove_userprofile_house_no'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='address_note',
            field=models.TextField(blank=True, help_text='(zvonček, poschodie, ...)', max_length=256, verbose_name='Poznámka pre kuriéra'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='city',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='country',
            field=models.CharField(blank=True, max_length=16),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='district',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='postal',
            field=models.CharField(blank=True, max_length=6),
        ),
    ]
