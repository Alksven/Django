from django.contrib.auth.models import Group
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
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
