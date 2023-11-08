from django.urls import path
from . import views

app_name = 'requestdataapp'
urlpatterns = [
    path("get", views.process_get_view, name='get-view'),
]