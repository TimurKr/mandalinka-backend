# Generated by Django 4.1 on 2023-03-18 18:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0013_ingredientversionstockorder_in_stock_amount'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ingredientversionstockorder',
            old_name='in_stock_amount',
            new_name='_in_stock_amount',
        ),
        migrations.AlterField(
            model_name='ingredientversionstockorder',
            name='parent',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, parent_link=True, primary_key=True, related_name='ordered', serialize=False, to='management.ingredientversionstockchange'),
        ),
        migrations.AddConstraint(
            model_name='ingredientversionstockorder',
            constraint=models.CheckConstraint(check=models.Q(models.Q(('_in_stock_amount', 0), ('is_delivered', False)), models.Q(('_in_stock_amount', 0), _negated=True), _connector='OR'), name='management_ingredientversionstockorder_in_stock_amount_is_0_if_is_delivered_is_false'),
        ),
    ]
