# Generated by Django 5.1 on 2024-10-09 12:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0005_customer_created_at_customer_created_by_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='address',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='customer',
            name='contact',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='customer',
            name='email',
            field=models.EmailField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='customer',
            name='phone',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='freight_price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.AddField(
            model_name='order',
            name='total_value',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
