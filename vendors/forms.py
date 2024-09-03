# vendors/forms.py

from django import forms
from .models import Vendor, VendorProduct, VendorOrder, VendorOrderItem

class VendorForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = ['name', 'address', 'phone']

class VendorProductForm(forms.ModelForm):
    class Meta:
        model = VendorProduct
        fields = ['name',]

class VendorOrderForm(forms.ModelForm):
    class Meta:
        model = VendorOrder
        fields = ['status']

class VendorOrderItemForm(forms.ModelForm):
    class Meta:
        model = VendorOrderItem
        fields = ['product', 'quantity']

    def __init__(self, *args, **kwargs):
        vendor = kwargs.pop('vendor', None)
        super().__init__(*args, **kwargs)
        if vendor:
            self.fields['product'].queryset = VendorProduct.objects.filter(vendor=vendor)
