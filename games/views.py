from django.shortcuts import render
from django.views.generic.base import TemplateView

from .forms import GameSearchForm
from .services import get_or_sync_game, search_games


class SearchGameView(TemplateView):
    template_name = "games/games-search.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = GameSearchForm(self.request.GET or None)
        games = []

        if form.is_valid():
            query = form.cleaned_data.get("q")
            if query:
                games = search_games(query).get("results")
                # with open("games/responses/games.json") as f:
                #     games = json.load(f)

        context["form"] = form
        context["games"] = games
        return context


def retrieve_game(request, slug):
    game = get_or_sync_game(slug)
    return render(request, "games/game-details.html", {"game": game})
