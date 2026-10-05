from django.shortcuts import render

from .services import get_or_fetch_game


# Create your views here.
def search_game(request):
    query = (request.GET.get("q") or "").strip()
    game = None
    if query:
        game = get_or_fetch_game(query)


    return render(request, "games/game-search.html", {"game": game })
