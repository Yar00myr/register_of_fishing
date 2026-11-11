import json
from functools import lru_cache
from pathlib import Path

COUNTRIES_FILE = Path(__file__).parent / "data" / "country.json"


@lru_cache(maxsize=1)
def load_countries() -> dict[str, str]:
    """Return ``{code: name}`` in the order of the JSON file."""
    with COUNTRIES_FILE.open(encoding="utf-8") as f:
        return {c["code"]: c["name"] for c in json.load(f)}


def get_country_choices() -> list[tuple[str, str]]:
    """Django ``choices`` callable (evaluated lazily by the model field)."""
    return list(load_countries().items())


def get_country_name(code: str) -> str:
    """Country name for ``code``; falls back to the code itself if unknown."""
    return load_countries().get(code, code)
