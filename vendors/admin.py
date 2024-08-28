from django.contrib import admin
from .models import Vendor, VendorProduct

admin.site.register(Vendor)
admin.site.register(VendorProduct)