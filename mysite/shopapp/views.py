from timeit import default_timer

from django.contrib.auth.models import Group
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView

from .models import Product, Order

from .forms import ProductForm, OrderForm, GroupForm

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin

class ShopIndexView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        products = [
            ("Laptop", 1999),
            ("Desktop", 2999),
            ("SmartPhone", 999),
        ]
        context = {
            "time_running": default_timer(),
            "products": products,
        }
        return render(request, "shopapp/shop-index.html", context=context)


class GroupsListView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        context = {
            "form": GroupForm(),
            "groups": Group.objects.prefetch_related('permissions').all(),
        }
        return render(request, "shopapp/groups_list.html", context=context)

    def post(self, request: HttpRequest):
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()

        return redirect(request.path)


class ProductDetailsView(DetailView):
    template_name = "shopapp/product-details.html"
    model = Product
    context_object_name = "product"


class ProductsListView(ListView):
    template_name = "shopapp/products-list.html"
    # model = Product
    context_object_name = 'products'
    queryset = Product.objects.filter(archived=False)


class ProductCreateView(PermissionRequiredMixin, CreateView):
    permission_required = "shopapp.add_product"
    model = Product
    fields = "name", "price", "description", "diccount", "preview"
    success_url = reverse_lazy("shopapp:products_list")

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class ProductUpdateView(UserPassesTestMixin, UpdateView):

    def test_func(self):
        obj = self.get_object()
        if (obj.created_by_id == self.request.user.pk or
            self.request.user.is_superuser or
            self.request.user.has_perm("shopapp.change_product")):
            return True
        return False

    model = Product
    fields = "name", "price", "description", "diccount", "preview"
    template_name_suffix = "_update_form"

    def get_success_url(self):
        return reverse("shopapp:products_details", kwargs={"pk": self.object.pk})


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy("shopapp:products_list")

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.archived = True
        self.object.save()
        return HttpResponseRedirect(success_url)


class OrderListView(LoginRequiredMixin, ListView):
    queryset = (
        Order.objects.select_related("user").prefetch_related("products")
    )


class OrderDetailsView(PermissionRequiredMixin, DetailView):
    permission_required = "shopapp.view_order"
    queryset = (
        Order.objects.select_related("user").prefetch_related("products")
    )

class OrderCreateView(CreateView):
    model = Order
    fields = "user", "products", "delivery_address", "promocode"
    success_url = reverse_lazy("shopapp:orders_list")


class OrderUpdateView(UpdateView):
    model = Order
    fields = "user", "products", "delivery_address", "promocode"
    template_name_suffix = "_update_form"

    def get_success_url(self):
        return reverse("shopapp:order_details", kwargs={"pk": self.object.pk})


class OrderDeleteView(DeleteView):
    model = Order
    success_url = reverse_lazy("shopapp:orders_list")




class ProductExportView(View):
    def get(self, request) -> JsonResponse:
        products = Product.objects.order_by("pk").all()
        products_data = [
            {
                "pk": product.pk,
                "name": product.name,
                "price": product.price,
                "archived": product.archived
            }
            for product in products
        ]
        return JsonResponse({"products": products_data})


class OrdersDataExportView(PermissionRequiredMixin, View):
    permission_required = "auth.view_user"

    def get(self, request: HttpRequest) -> JsonResponse:
        orders = Order.objects.order_by("pk").all()
        orders_data = [
            {
                "pk": order.pk,
                "delivery_address": order.delivery_address,
                "promocode": order.promocode,
                "user": order.user.id,
                "products": [product.id for product in order.products.all()]

            }
            for order in orders
        ]

        return JsonResponse({"orders": orders_data})



def shop_about(request: HttpRequest):
    text_about = "Наша Компания - ваш надежный партнер в мире электроники!" \
                 "Мы являемся лидерами в области продажи электроники и предлагаем широкий ассортимент качественных товаров по конкурентоспособным ценам." \
                 "Специализируемся на предоставлении клиентам самых современных и инновационных устройств от ведущих мировых производителей."
    context = {"text": text_about}
    return render(request, "shopapp/about.html", context=context)


def shop_contact(request: HttpRequest):
    addresses = [("Москва, ул Гагарина 123"),
               ("Санкт-Петербург, пр-т Невский 15"),
               ("Москва, ул. Иванова 44"),
    ]

    context = {
        "addresses": addresses,
    }
    return render(request, "shopapp/contacts.html", context=context)
