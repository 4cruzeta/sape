# customers/forms.py

from django import forms
from django.forms import inlineformset_factory
from django.utils.translation import gettext_lazy as _
from .models import Customer, Order, OrderItem

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'notes']
        labels = {
            'name': _('Name'),
            'notes': _('Notes'),
        }

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['customer', 'status', 'obs']
        labels = {
            'customer': _('Customer'),
            'status': _('Status'),
            'obs': _('Observations'),
        }

class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['inventory', 'quantity']
        labels = {
            'inventory': _('Inventory'),
            'quantity': _('Quantity'),
        }

OrderItemFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=1, can_delete=True)