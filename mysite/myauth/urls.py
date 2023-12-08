from django.contrib.auth.views import LoginView
from django.urls import path


from . import views

app_name = "myauth"
urlpatterns = [
    # path("login/", views.login_view, name="login"),
    path(
        "login/",
        LoginView.as_view(
            template_name='myauth/login.html',
            redirect_authenticated_user=True,
        ),
        name="login"),

    path("about-me/", views.AboutMeView.as_view(), name="about-me"),
    path("register/", views.RegisterView.as_view(), name="register"),

    # path("logout/", views.logout_view, name="logout"),
    path("logout/", views.MyLogoutView.as_view(), name="logout"),

    path("cookie/set/", views.set_cookie_view, name="cookie-set"),
    path("cookie/get/", views.get_cookie_view, name="cookie-get"),

    path("session/set/", views.set_session_view, name="session-set"),
    path("session/get/", views.get_session_view, name="session-get"),

    path("foo-bar", views.FooBarView.as_view(), name="foo-bar"),
]

