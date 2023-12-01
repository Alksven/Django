from django.contrib.auth.models import Group
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView

from .forms import ProductForm, GroupForm
from .models import Product, Order
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect, reverse, get_object_or_404
import timeit


class ShopIndexView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
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


class GroupsListView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        context = {
            "form": GroupForm(),
            'groups': Group.objects.prefetch_related('permissions').all(),
        }
        return render(request, 'shopapp/groups-list.html',  context=context)

    def post(self, request: HttpRequest) -> HttpResponse:
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect(request.path)


class ProductDetailsView(DetailView):
    template_name = 'shopapp/product-details.html'
    model = Product
    context_object_name = "products"


class ProductListVies(ListView):
    template_name = 'shopapp/products-list.html'
    model = Product
    context_object_name = "products"


class OrdersListVies(ListView):
    queryset = Order.objects.select_related('user').prefetch_related('products')


class OrderDetailsView(DetailView):
    queryset = Order.objects.select_related('user').prefetch_related('products')





def create_product(request: HttpRequest):
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            # name = form.cleaned_data["name"]
            # Product.objects.create(**form.cleaned_data)
            form.save()
            url = reverse("shopapp:products_list")
            return redirect(url)
    else:
        form = ProductForm()
    context = {
        'form': form
    }

    return render(request, 'shopapp/create-product.html',  context=context)



