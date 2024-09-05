# inventory/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from vendors.models import VendorOrder, VendorOrderItem
from .models import Inventory

@receiver(post_save, sender=VendorOrder)
def update_inventory(sender, instance, **kwargs):
    if instance.status == 'delivered':
        for item in VendorOrderItem.objects.filter(order=instance):
            inventory_item, created = Inventory.objects.get_or_create(
                name=item.product.name,
                defaults={'quantity': 0}
            )
            inventory_item.quantity += item.quantity
            inventory_item.save()