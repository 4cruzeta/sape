# inventory/signals.py

from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from vendors.models import VendorOrder, VendorOrderItem, VendorProduct
from .models import Inventory
from decimal import Decimal
from django.utils.translation import gettext as _
from django.utils import dateformat

@receiver(post_save, sender=VendorOrder)
def update_inventory(sender, instance, created, **kwargs):
    if not created and instance.status == 'delivered':
        # Check if the status has changed to 'delivered'
        if instance._previous_status != 'delivered':
            for item in VendorOrderItem.objects.filter(order=instance):
                # Fetch the VendorProduct instance
                vendor_product = VendorProduct.objects.get(name=item.product, vendor=instance.vendor)

                inventory_item, created = Inventory.objects.get_or_create(
                    product=item.product,
                    defaults={'quantity': 0, 'cost_price': Decimal('0.00'), 'description': ''}  # Set default cost_price and description
                )
                inventory_item.quantity += item.quantity

                # Calculate price_with_freight
                total_product_price = item.price * item.quantity
                apportioned_freight = (total_product_price / instance.total_value) * (instance.freight_price / item.quantity)
                itemPriceWithFreight = item.price + Decimal(apportioned_freight)
                
                total_cost = itemPriceWithFreight * item.quantity  # Calculate total cost for the item
                inventory_item.cost_price += total_cost  # Add the total cost to the existing cost_price
                
                # Fetch the description from the VendorProduct model
                product_description = vendor_product.description
                
                # Format the date and time to a more readable format in 24-hour format
                formatted_date = dateformat.format(instance.created_at, 'j N Y, H:i')  # Example: 'Jan 1, 2023, 14:25'

                # Prepare the new description line
                new_description_line = _(
                    "- Last bought from {vendor}, for ${price} each, in {date}"
                ).format(
                    vendor=instance.vendor,
                    quantity=item.quantity,
                    price=itemPriceWithFreight,
                    date=formatted_date,
                )

                # Append the new description to the existing one
                if inventory_item.description:
                    inventory_item.description += _("\n{new_description_line}\n").format(
                        new_description_line=new_description_line,
                    )
                else:
                    inventory_item.description = _("{new_description_line}\n").format(
                        new_description_line=new_description_line,
                    )
                                
                inventory_item.save()

# Connect the capture_previous_status function to the pre_save signal
def capture_previous_status(sender, instance, **kwargs):
    if instance.pk:
        instance._previous_status = sender.objects.get(pk=instance.pk).status
    else:
        instance._previous_status = None

pre_save.connect(capture_previous_status, sender=VendorOrder)