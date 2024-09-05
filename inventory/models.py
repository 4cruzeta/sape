# inventory/models.py

from django.db import models

class Inventory(models.Model):
    name = models.CharField(max_length=255)
    quantity = models.IntegerField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"