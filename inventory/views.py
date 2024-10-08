# inventory/views.py
import logging
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Inventory
from .forms import InventoryForm

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

@login_required(login_url="/users/login/")
def inventory_new(request):
    if request.method == 'POST':
        form = InventoryForm(request.POST)
        if form.is_valid():
            form.save()
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