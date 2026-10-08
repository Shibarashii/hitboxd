from math import ceil

from django.shortcuts import render
from django.views.generic.base import TemplateView

from .forms import GameSearchForm
from .services import PAGE_SIZE, get_or_sync_game, search_games


class SearchGameView(TemplateView):
    template_name = "games/games-search.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = GameSearchForm(self.request.GET or None)
        games = []

        if form.is_valid():
            query = form.cleaned_data.get("q")
            page = form.cleaned_data.get("page") or 1
            if query:
                data = search_games(query, page)
                games = data.get("results", [])
                context["page"] = page
                context["num_pages"] = ceil(data.get("count", 0) / PAGE_SIZE)
                context["has_previous"] = bool(data.get("previous"))
                context["has_next"] = bool(data.get("next"))
                # with open("games/responses/games.json") as f:
                #     games = json.load(f)

        context["form"] = form
        context["games"] = games
        return context


def retrieve_game(request, slug):
    game = get_or_sync_game(slug)
    return render(request, "games/game-details.html", {"game": game})
