from django.urls import path, re_path
from django.contrib.auth.decorators import login_required
from . import authentication


urlpatterns = [
    path("", authentication.loggin, name="loggin"),
    path("logout/", authentication.loggedout, name="logout"),
    re_path(r"^accounts/login/$", authentication.user_login, name="login"),
]