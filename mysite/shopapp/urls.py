from django.urls import path
from . import views

app_name = 'shopapp'
urlpatterns = [
    path("", views.ShopIndexView.as_view(), name='index'),
    path("groups/", views.GroupsListView.as_view(), name='groups_list'),
    path("products/", views.ProductListVies.as_view(), name='products_list'),
    path("products/<int:pk>/", views.ProductDetailsView.as_view(), name='product_details'),
    path("products/create/", views.ProductCreateVies.as_view(), name='product-create'),
    path("products/<int:pk>/update/", views.ProductUpdateVies.as_view(), name='product-update'),
    path("orders/", views.OrdersListVies.as_view(), name='orders_list'),
    path("orders/<int:pk>/", views.OrderDetailsView.as_view(), name='orders_details'),
]