# inventory/views.py
import logging
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Inventory
from .forms import InventoryForm
from django.utils import timezone
from django.utils.translation import gettext as _ 

# Configure logging
logger = logging.getLogger(__name__)

@login_required(login_url="/users/login/")
def inventory_list(request):
    inventory_items = Inventory.objects.all()
    return render(request, 'inventory/inventory_list.html', {'inventory_items': inventory_items})

@login_required(login_url="/users/login/")
def inventory_detail(request, pk):
    inventory_item = get_object_or_404(Inventory, pk=pk)
    return render(request, 'inventory/inventory_detail.html', {'inventory_item': inventory_item})

from django.utils import timezone

@login_required(login_url="/users/login/")
def inventory_new(request):
    if request.method == 'POST':
        form = InventoryForm(request.POST)
        if form.is_valid():
            product_name = form.cleaned_data['product']
            quantity = form.cleaned_data['quantity']
            cost_price = form.cleaned_data['cost_price']
            user = request.user  # Get the current user
            new_description = form.cleaned_data.get('description', '')  # Get the new description

            # Format the date
            formatted_date = timezone.now().strftime('%Y-%m-%d')

            # Prepare the new description line
            new_description_line = _(
                "- Last added by {user}, {quantity} items for ${price} each, on {date}, with description: {description}"
            ).format(
                user=user.username,
                price=cost_price,
                date=formatted_date,
                description=new_description,
                quantity=quantity,
            )

            # Check if the product already exists in the inventory
            try:
                inventory_item = Inventory.objects.get(product=product_name)
                # Update the existing product's quantity and cost price
                inventory_item.quantity += quantity
                inventory_item.cost_price += cost_price * quantity

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
                logger.info(f"Updated existing product: {product_name}")
            except Inventory.DoesNotExist:
                # Create a new product
                inventory_item = form.save(commit=False)
                inventory_item.description = _("{new_description_line}\n").format(
                    new_description_line=new_description_line,
                )
                inventory_item.save()
                logger.info(f"Added new product: {product_name}")
            
            return redirect('inventory_list')
    else:
        form = InventoryForm()
    return render(request, 'inventory/inventory_form.html', {'form': form})

@login_required(login_url="/users/login/")
def inventory_edit(request, pk):
    inventory_item = get_object_or_404(Inventory, pk=pk)
    if request.method == 'POST':
        form = InventoryForm(request.POST, instance=inventory_item)
        if form.is_valid():
            form.save()
            return redirect('inventory_detail', pk=inventory_item.pk)
    else:
        form = InventoryForm(instance=inventory_item)
    return render(request, 'inventory/inventory_form.html', {'form': form})