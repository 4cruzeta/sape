# customers/forms.py

from django import forms
from django.forms import inlineformset_factory
from .models import Customer, Order, OrderItem

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'notes']

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['customer', 'status', 'obs']

class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['inventory', 'quantity']

OrderItemFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=1, can_delete=True)