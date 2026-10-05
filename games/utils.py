import json
from collections.abc import Callable
from pathlib import Path

_CUR_DIR = Path(__file__).parent


def dump_response(filename: str = "response.json"):
    """
    Dump API Responses to a json file for debugging
    """
    def decorator(func: Callable):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            with open(_CUR_DIR / "responses" / filename, "w") as f:
                json.dump(result, f, indent=2)
            return result
        return wrapper
    return decorator
