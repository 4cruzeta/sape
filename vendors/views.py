# vendors/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Vendor, VendorProduct
from .forms import VendorForm, VendorProductForm

def vendor_list(request):
    vendors = Vendor.objects.all()
    return render(request, 'vendors/vendor_list.html', {'vendors': vendors})

def vendor_detail(request, pk):
    vendor = get_object_or_404(Vendor, pk=pk)
    return render(request, 'vendors/vendor_detail.html', {'vendor': vendor})

def vendor_new(request):
    if request.method == 'POST':
        form = VendorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('vendor_list')
    else:
        form = VendorForm()
    return render(request, 'vendors/vendor_form.html', {'form': form})

def vendor_edit(request, pk):
    vendor = get_object_or_404(Vendor, pk=pk)
    if request.method == 'POST':
        form = VendorForm(request.POST, instance=vendor)
        if form.is_valid():
            form.save()
            return redirect('vendor_list')
    else:
        form = VendorForm(instance=vendor)
    return render(request, 'vendors/vendor_form.html', {'form': form})

def vendorproduct_list(request, pk):
    vendorproducts = VendorProduct.objects.filter(vendor=pk)
    return render(request, 'vendors/vendorproduct_list.html', {'vendorproducts': vendorproducts})

def vendorproduct_detail(request, pk, vendorproduct_pk):
    vendorproduct = get_object_or_404(VendorProduct, pk=vendorproduct_pk)
    return render(request, 'vendors/vendorproduct_detail.html', {'vendorproduct': vendorproduct})

def vendorproduct_new(request, pk):
    if request.method == 'POST':
        form = VendorProductForm(request.POST)
        if form.is_valid():
            vendorproduct = form.save(commit=False)
            vendorproduct.vendor_id = pk
            vendorproduct.save()
            return redirect('products', pk=pk)
    else:
        form = VendorProductForm()
    return render(request, 'vendors/vendorproduct_form.html', {'form': form})

def vendorproduct_edit(request, pk, vendorproduct_pk):
    vendorproduct = get_object_or_404(VendorProduct, pk=vendorproduct_pk)
    if request.method == 'POST':
        form = VendorProductForm(request.POST, instance=vendorproduct)
        if form.is_valid():
            form.save()
            return redirect('vendorproduct_detail', pk=pk, vendorproduct_pk=vendorproduct_pk)
    else:
        form = VendorProductForm(instance=vendorproduct)
    return render(request, 'vendors/vendorproduct_form.html', {'form': form})