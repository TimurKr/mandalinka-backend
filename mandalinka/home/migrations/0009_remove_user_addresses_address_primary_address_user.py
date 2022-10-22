# Generated by Django 4.1 on 2022-10-22 17:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0008_alter_address_coordinates'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='addresses',
        ),
        migrations.AddField(
            model_name='address',
            name='primary',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='address',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='addresses', to=settings.AUTH_USER_MODEL),
        ),
    ]
