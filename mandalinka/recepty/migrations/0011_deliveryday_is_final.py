# Generated by Django 4.1 on 2022-10-02 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recepty', '0010_alter_deliveryday_recipes_alter_ingredient_img_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='deliveryday',
            name='is_final',
            field=models.BooleanField(default=False, help_text='If set to True, new orders will be created'),
        ),
    ]