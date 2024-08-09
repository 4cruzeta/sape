from django.db import models
from django.contrib.auth.models import User
from vendors.models import Vendor

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100, null=True)

    def __str__(self) -> str:
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField(null=True)
    barcode = models.CharField(max_length=50, null=True)
    description = models.CharField(max_length=200, null=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True)

    def __str__(self) -> str:
        return self.name

