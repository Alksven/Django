from django.urls import path
from . import views

app_name = "requestdataapp"
urlpatterns = [
    path("get/", views.process_get_views, name="get-vew"),
    path("bio/", views.user_form, name="user-form"),
    path("upload/", views.handle_file_upload, name="file-upload"),

]