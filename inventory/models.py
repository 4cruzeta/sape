# inventory/models.py

from django.db import models

class Inventory(models.Model):
    product = models.CharField(max_length=255)
    quantity = models.IntegerField()
    cost_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.product} - {self.quantity} - {self.cost_price}"

