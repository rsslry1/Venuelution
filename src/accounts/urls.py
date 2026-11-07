from django.contrib.auth.views import LogoutView
from django.urls import path

from . import views


app_name = "accounts"

urlpatterns = [
    path("login/", views.LoginPageView.as_view(), name="login"),
    path("signup/", views.signup_view, name="signup"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("dashboard/", views.dashboard_view, name="dashboard"),
]
