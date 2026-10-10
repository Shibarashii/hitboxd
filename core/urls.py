from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from . import views

urlpatterns = [
    path("", views.HomePageView.as_view(), name="homepage"),
    path("registration", views.SignUpView.as_view(), name="registration"),
    path("login", LoginView.as_view(template_name="core/login.html", redirect_authenticated_user=True), name="login"),
    path("logout", LogoutView.as_view(), name="logout"),
]
