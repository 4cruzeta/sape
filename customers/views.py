# customers/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Customer, Order, OrderItem
from .forms import CustomerForm, OrderForm, OrderItemForm, OrderItemFormSet
from inventory.models import Inventory

@login_required(login_url="/users/login/")
def customer_list(request):
    customers = Customer.objects.all()
    return render(request, 'customers/customer_list.html', {'customers': customers})

@login_required(login_url="/users/login/")
def customer_detail(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    return render(request, 'customers/customer_detail.html', {'customer': customer})

@login_required(login_url="/users/login/")
def customer_new(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer = form.save(commit=False)
            customer.created_by = request.user
            customer.updated_by = request.user
            customer.save()
            return redirect('customer_list')
    else:
        form = CustomerForm()
    return render(request, 'customers/customer_form.html', {'form': form})

@login_required(login_url="/users/login/")
def customer_edit(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            customer = form.save(commit=False)
            customer.updated_by = request.user
            customer.save()
            return redirect('customer_detail', pk=customer.pk)
    else:
        form = CustomerForm(instance=customer)
    return render(request, 'customers/customer_form.html', {'form': form})

@login_required(login_url="/users/login/")
def customer_delete(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        customer.delete()
        return redirect('customer_list')
    return render(request, 'customers/customer_confirm_delete.html', {'customer': customer})

@login_required(login_url="/users/login/")
def order_list(request):
    orders = Order.objects.all()
    return render(request, 'customers/order_list.html', {'orders': orders})

@login_required(login_url="/users/login/")
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order_items = order.orderitem_set.all()
    order_items_with_total = [
        {
            'inventory': item.inventory,
            'quantity': item.quantity,
            'price': item.price,
            'total': item.price * item.quantity
        }
        for item in order_items
    ]
    return render(request, 'customers/order_detail.html', {
        'order': order,
        'order_items': order_items_with_total
    })

@login_required(login_url="/users/login/")
def order_new(request):
    if request.method == 'POST':
        order_form = OrderForm(request.POST)
        formset = OrderItemFormSet(request.POST)
        if order_form.is_valid() and formset.is_valid():
            order = order_form.save(commit=False)
            order.created_by = request.user
            order.save()
            formset.instance = order
            formset.save()
            order.total_value = sum(form.calculate_total_value() for form in formset.forms)
            order.save()
            if order.status == 'confirmed':
                order.update_inventory()
            return redirect('order_edit', pk=order.pk)
    else:
        order_form = OrderForm()
        formset = OrderItemFormSet()
    return render(request, 'customers/order_form.html', {
        'order_form': order_form, 
        'formset': formset,
        'total_value': 0
    })

@login_required(login_url="/users/login/")
def order_edit(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        order_form = OrderForm(request.POST, instance=order)
        formset = OrderItemFormSet(request.POST, instance=order)
        if order_form.is_valid() and formset.is_valid():
            order_form.save()
            formset.save()
            order.total_value = sum(form.calculate_total_value() for form in formset.forms)
            order.save()
            if order.status == 'confirmed':
                order.update_inventory()
            return redirect('order_edit', pk=order.pk)
    else:
        order_form = OrderForm(instance=order)
        formset = OrderItemFormSet(instance=order)
    total_value = order.total_value
    return render(request, 'customers/order_form.html', {
        'order_form': order_form,
        'formset': formset,
        'total_value': total_value
    })

@login_required(login_url="/users/login/")
def order_delete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('order_list')
    return render(request, 'customers/order_confirm_delete.html', {'order': order})