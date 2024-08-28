# vendors/forms.py
from django import forms
from .models import Vendor, VendorProduct

class VendorForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = ('created_by', 'name', 'address', 'phone')

class VendorProductForm(forms.ModelForm):
    class Meta:
        model = VendorProduct
        fields = ('vendor', 'name')