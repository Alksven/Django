from django.urls import path
from . import views

app_name = 'shopapp'
urlpatterns = [
    path("", views.ShopIndexView.as_view(), name='index'),
    path("groups/", views.GroupsListView.as_view(), name='groups_list'),
    path("products/<int:pk>/", views.ProductDetailsView.as_view(), name='products_details'),
    path("products/", views.ProductListVies.as_view(), name='products_list'),
    path("products/create/", views.create_product, name='product-create'),
    path("orders/", views.orders_list, name='orders_list'),
]