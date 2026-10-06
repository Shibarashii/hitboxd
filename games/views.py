from django.shortcuts import render

from .forms import GameSearchForm
from .services import list_games, retrieve_game_details


# Create your views here.
def search_game(request):
    form = GameSearchForm(request.GET)
    games = []
    if form.is_valid():
        query = form.cleaned_data.get("q")
        if query:
            games = list_games(query)

    return render(
        request,
        "games/games-search.html",
        {
            "form": form,
            "games": games,
        },
    )


def retrieve_game(request, slug):
    game = retrieve_game_details(slug)
    return render(request, "games/game-details.html", {"game": game})
