from django.contrib.auth.views import LoginView
from django.urls import path
from . import views



app_name = 'myauth'
urlpatterns = [
    path("login/", LoginView.as_view(template_name="myauth/login.html", redirect_authentication_user=True), name='login'),

]