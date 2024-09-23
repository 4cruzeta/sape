# vendors/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.forms import inlineformset_factory
from .models import Vendor, VendorProduct, VendorOrder, VendorOrderItem
from .forms import VendorForm, VendorOrderForm, VendorOrderItemForm, VendorProductForm


@login_required(login_url="/users/login/")
def vendor_list(request):
    vendors = Vendor.objects.all()
    return render(request, 'vendors/vendor_list.html', {'vendors': vendors})

@login_required(login_url="/users/login/")
def vendor_detail(request, pk):
    vendor = get_object_or_404(Vendor, pk=pk)
    return render(request, 'vendors/vendor_detail.html', {'vendor': vendor})

@login_required(login_url="/users/login/")
def vendor_new(request):
    if request.method == 'POST':
        form = VendorForm(request.POST)
        if form.is_valid():
            vendor = form.save(commit=False)
            vendor.created_by = request.user
            vendor.save()
            return redirect('vendor_list')
    else:
        form = VendorForm()
    return render(request, 'vendors/vendor_form.html', {'form': form})

@login_required(login_url="/users/login/")
def vendor_edit(request, pk):
    vendor = get_object_or_404(Vendor, pk=pk)
    if request.method == 'POST':
        form = VendorForm(request.POST, instance=vendor)
        if form.is_valid():
            form.save()
            return redirect('vendor_detail', pk=vendor.pk)
    else:
        form = VendorForm(instance=vendor)
    return render(request, 'vendors/vendor_form.html', {'form': form})

def vendor_delete(request, pk):
    vendor = get_object_or_404(Vendor, pk=pk)
    if request.method == 'POST':
        vendor.delete()
        return redirect('vendor_list')
    return render(request, 'vendors/vendor_confirm_delete.html', {'vendor': vendor})

def vendorproduct_list(request, pk):
    vendor = get_object_or_404(Vendor, pk=pk)
    vendorproducts = VendorProduct.objects.filter(vendor=vendor)
    # print(vendorproducts.query)  # Print the SQL query to the console for debugging
    return render(request, 'vendors/vendorproduct_list.html', {'vendor': vendor, 'vendorproducts': vendorproducts})

def vendorproduct_detail(request, pk, vendorproduct_pk):
    vendorproduct = get_object_or_404(VendorProduct, pk=vendorproduct_pk)
    return render(request, 'vendors/vendorproduct_detail.html', {'vendorproduct': vendorproduct})

def vendorproduct_new(request, pk):
    vendor = get_object_or_404(Vendor, pk=pk)
    if request.method == 'POST':
        form = VendorProductForm(request.POST)
        if form.is_valid():
            vendorproduct = form.save(commit=False)
            vendorproduct.vendor = vendor
            vendorproduct.save()
            return redirect('products', pk=pk)
    else:
        form = VendorProductForm()
    return render(request, 'vendors/vendorproduct_form.html', {'form': form, 'vendor': vendor})

def vendorproduct_edit(request, pk, vendorproduct_pk):
    vendor = get_object_or_404(Vendor, pk=pk)
    vendorproduct = get_object_or_404(VendorProduct, pk=vendorproduct_pk)
    if request.method == 'POST':
        form = VendorProductForm(request.POST, instance=vendorproduct)
        if form.is_valid():
            form.save()
            return redirect('vendorproduct_detail', pk=pk, vendorproduct_pk=vendorproduct_pk)
    else:
        form = VendorProductForm(instance=vendorproduct)
    return render(request, 'vendors/vendorproduct_form.html', {'form': form, 'vendor': vendor})

def vendorproduct_delete(request, pk, vendorproduct_pk):
    vendorproduct = get_object_or_404(VendorProduct, pk=vendorproduct_pk)
    vendorproduct.delete()
    return redirect('products', pk=pk)

@login_required(login_url="/users/login/")
def vendor_order_new(request, vendor_id):
    vendor = get_object_or_404(Vendor, pk=vendor_id)
    VendorOrderItemFormSet = inlineformset_factory(VendorOrder, VendorOrderItem, form=VendorOrderItemForm, extra=1, can_delete=True)

    if request.method == 'POST':
        order_form = VendorOrderForm(request.POST)
        formset = VendorOrderItemFormSet(request.POST, form_kwargs={'vendor': vendor})
        if order_form.is_valid() and formset.is_valid():
            vendor_order = order_form.save(commit=False)
            vendor_order.vendor = vendor
            vendor_order.created_by = request.user
            vendor_order.save()

            formset.instance = vendor_order
            formset.save()

            return redirect('vendor_order_edit', vendor_id=vendor.id, order_id=vendor_order.id)
    else:
        order_form = VendorOrderForm()
        formset = VendorOrderItemFormSet(form_kwargs={'vendor': vendor})
    
    return render(request, 'vendors/vendor_order_form.html', {'order_form': order_form, 'formset': formset, 'vendor': vendor})

@login_required(login_url="/users/login/")
def vendor_order_edit(request, vendor_id, order_id):
    vendor = get_object_or_404(Vendor, pk=vendor_id)
    order = get_object_or_404(VendorOrder, pk=order_id, vendor=vendor)
    VendorOrderItemFormSet = inlineformset_factory(VendorOrder, VendorOrderItem, form=VendorOrderItemForm, extra=1, can_delete=True)

    if request.method == 'POST':
        order_form = VendorOrderForm(request.POST, instance=order)
        formset = VendorOrderItemFormSet(request.POST, instance=order, form_kwargs={'vendor': vendor})
        if order_form.is_valid() and formset.is_valid():
            order_form.save()
            formset.save()
            return redirect('vendor_order_edit', vendor_id=vendor.id, order_id=order.id)
    else:
        order_form = VendorOrderForm(instance=order)
        formset = VendorOrderItemFormSet(instance=order, form_kwargs={'vendor': vendor})
    
    return render(request, 'vendors/vendor_order_form.html', {'order_form': order_form, 'formset': formset, 'vendor': vendor})

@login_required(login_url="/users/login/")
def vendor_order_list(request, vendor_id):
    vendor = get_object_or_404(Vendor, pk=vendor_id)
    vendor_orders = VendorOrder.objects.filter(vendor=vendor)
    print(f"Vendor orders: {vendor_orders}")
    return render(request, 'vendors/vendor_order_list.html', {'vendor': vendor, 'vendor_orders': vendor_orders})

@login_required(login_url="/users/login/")
def vendor_order_detail(request, vendor_id, order_id):
    vendor = get_object_or_404(Vendor, pk=vendor_id)
    order = get_object_or_404(VendorOrder, pk=order_id, vendor=vendor)
    return render(request, 'vendors/vendor_order_detail.html', {'vendor': vendor, 'order': order})

@login_required(login_url="/users/login/")
def vendor_order_delete(request, vendor_id, order_id):
    vendor_order = get_object_or_404(VendorOrder, pk=order_id, vendor_id=vendor_id)
    if request.method == 'POST':
        vendor_order.delete()
        return redirect('vendor_order_list', vendor_id=vendor_id)
    return render(request, 'vendors/vendor_order_confirm_delete.html', {'vendor_order': vendor_order})