# Generated by Django 5.1 on 2024-09-23 20:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0003_rename_name_inventory_product'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='inventory',
            options={},
        ),
        migrations.AddField(
            model_name='inventory',
            name='cost_price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
