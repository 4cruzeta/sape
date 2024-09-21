# vendors/models.py

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Vendor(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    email = models.EmailField(max_length=255, blank=True, null=True)
    contact = models.CharField(max_length=255, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='vendors_created')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='vendors_updated')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = 'Vendor'
        verbose_name_plural = 'Vendors'

class VendorProduct(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    bar_code = models.CharField(max_length=255, blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='vendor_products_created')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='vendor_products_updated')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = 'Vendor Product'
        verbose_name_plural = 'Vendor Products'

class VendorOrder(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
    ]
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='vendor_orders_created')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='vendor_orders_updated')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"Order {self.id} by {self.created_by.username if self.created_by else 'Unknown'} for {self.vendor.name}"

    class Meta:
        verbose_name = 'Vendor Order'
        verbose_name_plural = 'Vendor Orders'

class VendorOrderItem(models.Model):
    order = models.ForeignKey(VendorOrder, on_delete=models.CASCADE)
    product = models.ForeignKey(VendorProduct, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    expiry_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.quantity} of {self.product.name} in order {self.order.id}"