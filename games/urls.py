from django.urls import path

from . import views

urlpatterns = [
    path("<slug:slug>", views.retrieve_game, name="game-details"),
    path("search/", views.search_game, name="search-games"),
]
