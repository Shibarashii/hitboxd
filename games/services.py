from core.utils import TerminalColors as tc

from .models import Game, Genre
from .rawg_client import fetch_games, fetch_single_game


def search_games(query: str | None):
    games = fetch_games(search=query)
    return games

def get_or_sync_game(slug: str):
    try:
        game = Game.objects.get(slug=slug)
        print(f"{tc.GREEN}Cache hit for {game.name.upper()}.{tc.RESET}")
        return game

    except Game.DoesNotExist:
        print(f"{tc.RED}Cache miss. Game is not found in database.{tc.RESET}")
        print("Retrieving game details...")
        fetched_game_details = fetch_single_game(slug_or_id=slug)

        if not fetched_game_details or not fetched_game_details.get("id"):
            print(f"{tc.RED}Game does not exist on RAWG.{tc.RESET}")
            return None

        print(f"Inserting {fetched_game_details.get('name')} into database...")
        game = Game.objects.create(
            rawg_id=fetched_game_details.get("id"),
            name=fetched_game_details.get("name"),
            slug=fetched_game_details.get("slug"),
            cover_url=fetched_game_details.get("background_image") or "",
            release_date=fetched_game_details.get("released") or None,
            summary=fetched_game_details.get("description_raw") or "",
        )

        fetched_genres = fetched_game_details.get("genres") or []

        for fgenre in fetched_genres:
            genre, _ = Genre.objects.get_or_create(
                rawg_id=fgenre.get("id"),
                defaults={"name": fgenre.get("name"), "slug": fgenre.get("slug")},
            )
            game.genres.add(genre)

        print(f"{tc.GREEN}Successfully added {game.name} to database.{tc.RESET}")

        return game
