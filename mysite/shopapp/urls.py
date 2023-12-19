from django.urls import path
from . import views

app_name = "shopapp"
urlpatterns = [
    path("", views.ShopIndexView.as_view(), name="index"),
    path("groups/", views.GroupsListView.as_view(), name="groups_list"),
    path("products/", views.ProductsListView.as_view(), name="products_list"),
    path("products/export/", views.ProductExportView.as_view(), name="products-export"),
    path("products/<int:pk>/", views.ProductDetailsView.as_view(), name="products_details"),
    path("products/create/", views.ProductCreateView.as_view(), name="product_create"),
    path("products/<int:pk>/update/", views.ProductUpdateView.as_view(), name="product_update"),
    path("products/<int:pk>/archive/", views.ProductDeleteView.as_view(), name="product_delete"),

    path("orders/", views.OrderListView.as_view(), name="orders_list"),
    path("orders/export/", views.OrdersDataExportView.as_view(), name="orders_export"),
    path("orders/<int:pk>/", views.OrderDetailsView.as_view(), name="order_details"),
    path("orders/create/", views.OrderCreateView.as_view(), name="order_create"),
    path("orders/<int:pk>/update/", views.OrderUpdateView.as_view(), name="order_update"),
    path("orders/<int:pk>/archive/", views.OrderDeleteView.as_view(), name="order_delete"),

    path("about/", views.shop_about, name="about"),
    path("contact/", views.shop_contact, name="contact"),
]