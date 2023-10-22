from django.http import HttpResponse
from django.shortcuts import render
import timeit


def shop_index(request):
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
