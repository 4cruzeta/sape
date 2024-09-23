# inventory/signals.py

from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from vendors.models import VendorOrder, VendorOrderItem
from .models import Inventory
from decimal import Decimal

@receiver(pre_save, sender=VendorOrder)
def capture_previous_status(sender, instance, **kwargs):
    if instance.pk:
        instance._previous_status = VendorOrder.objects.get(pk=instance.pk).status
    else:
        instance._previous_status = None

@receiver(post_save, sender=VendorOrder)
def update_inventory(sender, instance, created, **kwargs):
    if not created and instance.status == 'delivered':
        # Check if the status has changed to 'delivered'
        if instance._previous_status != 'delivered':
            for item in VendorOrderItem.objects.filter(order=instance):
                inventory_item, created = Inventory.objects.get_or_create(
                    product=item.product,
                    defaults={'quantity': 0, 'cost_price': Decimal('0.00')}  # Set default cost_price to Decimal
                )
                inventory_item.quantity += item.quantity
                total_cost = Decimal(item.price) * item.quantity  # Calculate total cost for the item
                inventory_item.cost_price += total_cost  # Add the total cost to the existing cost_price
                inventory_item.save()