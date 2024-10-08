# inventory/admin.py

from django.contrib import admin
from .models import Inventory

class InventoryAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity')

admin.site.register(Inventory, InventoryAdmin)
