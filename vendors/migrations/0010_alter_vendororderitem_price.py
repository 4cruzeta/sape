# Generated by Django 5.1 on 2024-09-22 19:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendors', '0009_vendororderitem_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vendororderitem',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
