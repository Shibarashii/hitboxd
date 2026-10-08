import os
from pathlib import Path

import requests
from dotenv import load_dotenv

from .utils import dump_response

load_dotenv()

_FILE_PATH = Path(__file__).parent
_BASE_URL = "https://api.rawg.io/api"
_API_KEY = os.getenv("RAWG_API_KEY")


@dump_response("games.json")
def fetch_games(**kwargs) -> list:
    """
    Fetch a list of games.

    Args:
        search (str): Seach query.

    Returns:
        List of games.
    """
    try:
        response = requests.get(
            f"{_BASE_URL}/games",
            params={"key": _API_KEY, **kwargs},
            timeout=5,
        )
        response.raise_for_status()
        # print(json.dumps(response.json(), indent=2))
        return response.json()
    except requests.RequestException:
        return []


@dump_response("game-details.json")
def fetch_single_game(slug_or_id: int | str) -> dict:
    """
    Fetch a game using an id or slug.
    """
    try:
        response = requests.get(
            f"{_BASE_URL}/games/{slug_or_id}",
            params={"key": _API_KEY},
            timeout=5,
        )
        response.raise_for_status()
        # print(json.dumps(response.json(), indent=2))
        return response.json()
    except requests.RequestException:
        return {}


if __name__ == "__main__":
    # list_games(search="Elden ring")
    game_details = fetch_single_game("elden-ring")
    rawg_id = game_details.get("id")
    name = game_details.get("name")
    slug = game_details.get("slug")
    cover_url = game_details.get("background_image") or None
    release_date = game_details.get("released") or None
    summary = game_details.get("description_raw") or None
    genres = game_details.get("genres") or []

    print(f"""
          {rawg_id}
          {name}
          {slug}
          {cover_url}
          {release_date}
          {summary}
          {type(genres)}
          """)

    for genre in genres:
        print(genre.get("id"))
        print(genre.get("slug"))
        print(genre.get("name"))
