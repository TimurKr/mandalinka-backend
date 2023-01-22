# Generated by Django 4.1 on 2023-01-04 17:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0019_alter_ingredientinstance_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='errors',
            field=models.CharField(default='', editable=False, help_text='String of IDs representing statuses separated by commas', max_length=10, verbose_name='Status'),
        ),
    ]