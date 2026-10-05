from core.utils import TerminalColors as tc

from .models import Game, Genre
from .rawg_client import retrieve_game


def get_or_fetch_game(slug: str):
    try:
        game = Game.objects.get(slug=slug)
        print(f"{tc.GREEN}Cache hit for {game.name.upper()}.{tc.RESET}")
        return game
    
    except Game.DoesNotExist:
        print(f"{tc.RED}Cache miss. Game does not found in database.{tc.RESET}")
        print("Retrieving game details...")
        rawg_game_details = retrieve_game(slug_or_id=slug)

        if not rawg_game_details or not rawg_game_details.get("id"):
            print(f"{tc.RED}Game does not exist on RAWG.{tc.RESET}")
            return None

        print(f"Inserting {rawg_game_details.get("name")} into database...")
        game = Game.objects.create(
            rawg_id=rawg_game_details.get("id"),
            name=rawg_game_details.get("name"),
            slug=rawg_game_details.get("slug"),
            cover_url=rawg_game_details.get("background_image") or "",
            release_date=rawg_game_details.get("released") or None,
            summary=rawg_game_details.get("description_raw") or "",
        )

        genres = rawg_game_details.get("genres") or []

        for g in genres:
            genre, _ = Genre.objects.get_or_create(
                rawg_id=g.get("id"),
                defaults={"name": g.get("name"), "slug": g.get("slug")},
            )
            game.genres.add(genre)

        print(f"{tc.GREEN}Successfully added {game.name} to database.{tc.RESET}")

        return game
