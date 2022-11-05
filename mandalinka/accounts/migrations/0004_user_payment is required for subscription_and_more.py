# Generated by Django 4.1 on 2022-11-05 19:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_user_is_active_alter_user_is_email_valid_and_more'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='user',
            constraint=models.CheckConstraint(check=models.Q(models.Q(('is_payment_valid', True), ('is_subscribed', True)), ('is_subscribed', False), _connector='OR'), name='payment is required for subscription'),
        ),
        migrations.AddConstraint(
            model_name='user',
            constraint=models.CheckConstraint(check=models.Q(models.Q(('is_email_valid', True), ('is_payment_valid', True)), ('is_payment_valid', False), _connector='OR'), name='Email confirmation is required for adding payment method'),
        ),
    ]