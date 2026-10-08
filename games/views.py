from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.decorators.cache import cache_control
import json

from .forms import GameSearchForm
from .services import get_or_sync_game, search_games


class SearchGameView(TemplateView):
    template_name = "games/games-search.html"

    def get_context_data(self, **kwargs) :
        context = super().get_context_data(**kwargs)
        form = GameSearchForm(self.request.GET or None)
        games = []

        if form.is_valid():
            query = form.cleaned_data.get("q")
            if query:
                games = search_games(query)

        context["form"] = form
        context["games"] = games
        return context


# Create your views here.
# def search_game(request):
#     form = GameSearchForm(request.GET)
#     games = []
#     if form.is_valid():
#         query = form.cleaned_data.get("q")
#         if query:
#             games = list_games(query)
#
#     return render(
#         request,
#         "games/games-search.html",
#         {
#             "form": form,
#             "games": games,
#         },
#     )


@cache_control(max_age=3600, public=True)
def retrieve_game(request, slug):
    # game = get_or_sync_game(slug)
    with open("games/responses/game-details.json") as f:
        game = json.load(f)
    return render(request, "games/game-details.html", {"game": game})
