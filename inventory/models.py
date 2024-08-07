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
    name = models.CharField(max_length=100, blank=False)
    category = models.CharField(max_length=20, choices=CATEGORY, blank=False)
    quantity = models.PositiveIntegerField(blank=False)
    barcode = models.CharField(max_length=50, blank=True)
    description = models.CharField(max_length=200, blank=True)

    def __str__(self) -> str:
        return self.name