from django.shortcuts import render, redirect
from .models import Vendor
from django.contrib.auth.decorators import login_required
from .forms import VendorForm 

@login_required(login_url="/users/login/")
def vendors(request):
    vendors = Vendor.objects.all()
    if request.method == 'POST':
        form = VendorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('vendors')
    else:
        form = VendorForm()
    context = {
        "title": "Vendors",
        "vendors": vendors,
        "form": form
    }
    return render(request, 'vendors/vendors.html', context)