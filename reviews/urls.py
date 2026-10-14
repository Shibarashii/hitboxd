from django.urls import path

from . import views

urlpatterns = [
        path("<slug:slug>/rate/", views.RateView.as_view(), name="rate-game")
]

