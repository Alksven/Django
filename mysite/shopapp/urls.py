from django.urls import path
from . import views

app_name = 'shopapp'
urlpatterns = [
    path("", views.shop_index, name='index'),
    path("groups/", views.groups_list, name='groups_list'),
    path("products/", views.products_list, name='products_list'),
    path("products/create/", views.create_product, name='product-create'),
    path("orders/", views.orders_list, name='orders_list'),
]