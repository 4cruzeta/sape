# customers/models.py

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from inventory.models import Inventory

class Customer(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
    ]
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"Order {self.id} for {self.customer.name}"

    def update_inventory(self):
        if self.status == 'confirmed':
            order_items = self.orderitem_set.all()
            for item in order_items:
                inventory_item = item.inventory
                # print(f"Decreasing inventory for {inventory_item.product} by {item.quantity}")
                inventory_item.quantity -= item.quantity
                inventory_item.save()

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    inventory = models.ForeignKey(Inventory, null=True, on_delete=models.SET_NULL)
    quantity = models.IntegerField()

    def __str__(self):
        return f"{self.quantity} of {self.inventory.product if self.inventory else 'Unknown'} in order {self.order.id}"

@receiver(post_save, sender=Order)
def update_inventory_on_confirm(sender, instance, **kwargs):
    if instance.status == 'confirmed':
        instance.update_inventory()