# customers/models.py

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from inventory.models import Inventory
from django.utils.translation import gettext_lazy as _

class Customer(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(max_length=255, blank=True, null=True)
    contact = models.CharField(max_length=255, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='customer_created')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='customer_updated')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', _('Pending')),
        ('confirmed', _('Confirmed')),
        ('shipped', _('Shipped')),
        ('delivered', _('Delivered')),
    ]
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending')
    freight_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    total_value = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    obs = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='customer_orders_created')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='customer_orders_updated')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

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
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    quantity = models.IntegerField()

    def __str__(self):
        return f"{self.quantity} of {self.inventory.product if self.inventory else 'Unknown'} in order {self.order.id}"

@receiver(post_save, sender=Order)
def update_inventory_on_confirm(sender, instance, **kwargs):
    if instance.status == 'confirmed':
        instance.update_inventory()