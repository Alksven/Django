from django.urls import path
from . import views

app_name = 'myauth'
urlpatterns = [
    path("login/", views.login_view, name='login'),

]