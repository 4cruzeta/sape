# Generated by Django 5.1 on 2024-09-22 19:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendors', '0007_alter_vendor_created_at_alter_vendor_updated_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vendororderitem',
            name='product',
            field=models.CharField(max_length=255),
        ),
    ]
