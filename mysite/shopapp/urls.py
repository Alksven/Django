from django.urls import path
from . import views

app_name = 'shopapp'
urlpatterns = [
    path("", views.shop_index, name='index'),

]