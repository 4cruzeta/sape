# vendors/forms.py

from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Vendor, VendorProduct, VendorOrder, VendorOrderItem

class VendorForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = ['name', 'address', 'phone', 'email', 'contact', 'notes']
        labels = {
            'name': _('Name'),
            'address': _('Address'),
            'phone': _('Phone'),
            'email': _('Email'),
            'contact': _('Contact'),
            'notes': _('Notes'),
        }

class VendorProductForm(forms.ModelForm):
    class Meta:
        model = VendorProduct
        fields = ['name', 'price', 'description', 'bar_code']
        labels = {
            'name': _('Name'),
            'price': _('Price'),
            'description': _('Description'),
            'bar_code': _('Bar Code'),
        }

class VendorOrderForm(forms.ModelForm):
    class Meta:
        model = VendorOrder
        fields = ['status', 'freight_price', 'obs']
        labels = {
            'status': _('Status'),
            'freight_price': _('Freight Price'),
            'obs': _('Observations'),
        }

class VendorOrderItemForm(forms.ModelForm):
    class Meta:
        model = VendorOrderItem
        fields = ['product', 'price', 'quantity']
        labels = {
            'product': _('Product'),
            'price': _('Price'),
            'quantity': _('Quantity'),
        }

    def __init__(self, *args, **kwargs):
        vendor = kwargs.pop('vendor', None)
        super().__init__(*args, **kwargs)
        if vendor:
            product_choices = [('', '---')] + [(product.name, product.name) for product in VendorProduct.objects.filter(vendor=vendor)]
            self.fields['product'].widget = forms.Select(choices=product_choices)
        self.fields['price'].widget.attrs['readonly'] = True  # Make price field read-only
        self.fields['price'].widget.attrs['class'] = 'price-field'  # Add class for JavaScript