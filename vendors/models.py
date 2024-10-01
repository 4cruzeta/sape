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
    freight_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_value = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    obs = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='vendor_orders_created')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='vendor_orders_updated')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    def calculate_total_value(self):
        total = sum(item.price * item.quantity for item in self.vendororderitem_set.all())
        self.total_value = total

    @property
    def total_value_plus_freight(self):
        return self.total_value + self.freight_price

    def save(self, *args, **kwargs):
        # Save the instance first to ensure it has a primary key
        super().save(*args, **kwargs)
        # Calculate the total value and save again
        self.calculate_total_value()
        super().save(update_fields=['total_value'])
        
    def __str__(self):
        return f"Order {self.id} by {self.created_by.username if self.created_by else 'Unknown'} for {self.vendor.name}"

    class Meta:
        verbose_name = 'Vendor Order'
        verbose_name_plural = 'Vendor Orders'

class VendorOrderItem(models.Model):
    order = models.ForeignKey(VendorOrder, on_delete=models.CASCADE)
    product = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    quantity = models.PositiveIntegerField()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.order.calculate_total_value()
        self.order.save(update_fields=['total_value'])

    def delete(self, *args, **kwargs):
        order = self.order
        super().delete(*args, **kwargs)
        order.calculate_total_value()
        order.save(update_fields=['total_value'])
