from django.shortcuts import render, redirect
from .models import Product
from django.contrib.auth.decorators import login_required
from .forms import ProductForm 

# Create your views here.

@login_required
def products(request):
    products = Product.objects.all()
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            try:
                product = Product.objects.get(name=name)
                add_form = ProductForm(request.POST)
                if add_form.is_valid():
                    product.quantity += add_form.cleaned_data['quantity']
                    product.save()
                else:
                    return render(request, 'products/products.html', context)
            except Product.DoesNotExist:
                form.save()
            return redirect('products')
    else:
        form = ProductForm()
    context = {
        "title": "Products",
        "products": products,
        "form": form
    }
    return render(request, 'products/products.html', context)