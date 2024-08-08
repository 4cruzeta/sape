from django.db import models
from django.contrib.auth.models import User

# Create your models here.

CATEGORY = (
    ('Stationary', 'Stationary'),
    ('Electronics', 'Electronics'),
    ('Food', 'Food'),
    ('Limpeza', 'Limpeza')
)

class Product(models.Model):
    name = models.CharField(max_length=100, null=True)
    category = models.CharField(max_length=20, choices=CATEGORY, null=True)
    quantity = models.PositiveIntegerField(null=True)
    barcode = models.CharField(max_length=50, null=True)
    description = models.CharField(max_length=200, null=True)

    def __str__(self) -> str:
        return self.name