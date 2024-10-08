# Generated by Django 5.1 on 2024-09-02 19:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendors', '0002_vendororder'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vendororder',
            name='quantity',
        ),
        migrations.CreateModel(
            name='VendorOrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vendors.vendororder')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vendors.vendorproduct')),
            ],
        ),
    ]
