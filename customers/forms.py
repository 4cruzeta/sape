# customers/forms.py

from django import forms
from django.forms import inlineformset_factory
from django.utils.translation import gettext_lazy as _
from .models import Customer, Order, OrderItem

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'address', 'phone', 'email', 'contact', 'notes']
        labels = {
            'name': _('Name'),
            'address': _('Address'),
            'phone': _('Phone'),
            'email': _('Email'),
            'contact': _('Contact'),
            'notes': _('Notes'),
        }
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 4}),
        }

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['customer', 'status', 'freight_price', 'total_value', 'obs']
        labels = {
            'customer': _('Customer'),
            'status': _('Status'),
            'freight_price': _('Freight Price'),
            'total_value': _('Total Value'),
            'obs': _('Observations'),
        }
        widgets = {
            'obs': forms.Textarea(attrs={'rows': 4}),
            'total_value': forms.TextInput(attrs={'readonly': 'readonly'}),
        }

class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['inventory', 'quantity', 'price']
        labels = {
            'inventory': _('Inventory'),
            'quantity': _('Quantity'),
            'price': _('Price'),
        }
        widgets = {
            'price': forms.TextInput(attrs={'readonly': 'readonly'}),
        }

    def save(self, commit=True):
        instance = super().save(commit=False)
        if instance.inventory:
            instance.price = instance.inventory.cost_price / instance.inventory.quantity
        if commit:
            instance.save()
        return instance

    def calculate_total_value(self):
        price = self.instance.price or 0
        quantity = self.instance.quantity or 0
        freight_price = self.instance.order.freight_price or 0
        return price * quantity + freight_price

OrderItemFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=1, can_delete=True)