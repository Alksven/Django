from django.contrib.auth.models import Group

from .forms import ProductForm
from .models import Product, Order
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect, reverse
import timeit


def shop_index(request: HttpRequest):
    products = [
        ('Laptop', 1990),
        ('Desktop', 2990),
        ("Smartphone", 990)
    ]
    context = {
        "time": timeit.default_timer(),
        "products": products,
    }
    return render(request, 'shopapp/shop-index.html', context=context)


def groups_list(request: HttpRequest):
    context = {
        'groups': Group.objects.prefetch_related('permissions').all(),
    }

    return render(request, 'shopapp/groups-list.html',  context=context)


def products_list(request: HttpRequest):
    context = {
        'products': Product.objects.all(),
    }

    return render(request, 'shopapp/products-list.html',  context=context)


def orders_list(request: HttpRequest):
    context = {
        'orders': Order.objects.select_related('user').prefetch_related('products').all(),
    }

    return render(request, 'shopapp/orders-list.html',  context=context)


def create_product(request: HttpRequest):
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            # name = form.cleaned_data["name"]
            Product.objects.create(**form.cleaned_data)
            url = reverse("shopapp:products_list")
            return redirect(url)
    else:
        form = ProductForm()
    context = {
        'form': form
    }

    return render(request, 'shopapp/create-product.html',  context=context)
