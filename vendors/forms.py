# vendors/forms.py

from django import forms
from .models import Vendor, VendorProduct, VendorOrder, VendorOrderItem

class VendorForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = ['name', 'address', 'phone', 'email', 'contact', 'notes']

class VendorProductForm(forms.ModelForm):
    class Meta:
        model = VendorProduct
        fields = ['name', 'price', 'description', 'bar_code']

class VendorOrderForm(forms.ModelForm):
    class Meta:
        model = VendorOrder
        fields = ['status', 'freight_price', 'obs']

class VendorOrderItemForm(forms.ModelForm):
    class Meta:
        model = VendorOrderItem
        fields = ['product', 'price', 'quantity']  

    def __init__(self, *args, **kwargs):
        vendor = kwargs.pop('vendor', None)
        super().__init__(*args, **kwargs)
        if vendor:
            product_choices = [('', '---')] + [(product.name, product.name) for product in VendorProduct.objects.filter(vendor=vendor)]
            self.fields['product'].widget = forms.Select(choices=product_choices)
        self.fields['price'].widget.attrs['readonly'] = True  # Make price field read-only
        self.fields['price'].widget.attrs['class'] = 'price-field'  # Add class for JavaScript