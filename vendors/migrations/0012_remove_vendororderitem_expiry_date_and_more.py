# Generated by Django 5.1 on 2024-09-23 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendors', '0011_vendororder_total_value_alter_vendororderitem_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vendororderitem',
            name='expiry_date',
        ),
        migrations.AlterField(
            model_name='vendororderitem',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='vendororderitem',
            name='quantity',
            field=models.PositiveIntegerField(),
        ),
    ]
