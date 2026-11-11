import json

import pytest

from main import countries
from main.models import FishingTrip


@pytest.fixture(autouse=True)
def clear_countries_cache():
    """The loader is cached, so every test starts and ends with a cold cache."""
    countries.load_countries.cache_clear()
    yield
    countries.load_countries.cache_clear()


@pytest.fixture
def countries_file(tmp_path, monkeypatch):
    """Point the loader at a small temporary JSON file."""
    path = tmp_path / "countries.json"
    path.write_text(
        json.dumps(
            [{"code": "PL", "name": "Poland"}, {"code": "AT", "name": "Austria"}]
        ),
        encoding="utf-8",
    )
    monkeypatch.setattr(countries, "COUNTRIES_FILE", path)
    return path


@pytest.mark.parametrize(
    ("code", "name"),
    [("UA", "Ukraine"), ("PL", "Poland"), ("GB", "United Kingdom")],
)
def test_known_code_returns_name(code, name):
    assert countries.get_country_name(code) == name


@pytest.mark.parametrize("code", ["ZZ", "", "ua"])
def test_unknown_code_falls_back_to_code(code):
    assert countries.get_country_name(code) == code


def test_choices_contain_real_data():
    assert ("UA", "Ukraine") in countries.get_country_choices()


def test_choices_keep_file_order(countries_file):
    assert countries.get_country_choices() == [("PL", "Poland"), ("AT", "Austria")]


def test_file_is_read_only_once(countries_file):
    countries.get_country_choices()
    countries_file.unlink()  

    assert countries.get_country_name("AT") == "Austria"
    assert countries.load_countries.cache_info().hits >= 1


def test_nothing_is_loaded_until_first_use():
    assert countries.load_countries.cache_info().currsize == 0


def test_cache_clear_picks_up_changed_file(countries_file):
    assert countries.get_country_name("PL") == "Poland"

    countries_file.write_text(
        json.dumps([{"code": "PL", "name": "Polska"}]), encoding="utf-8"
    )
    countries.load_countries.cache_clear()

    assert countries.get_country_name("PL") == "Polska"


def test_model_field_choices_come_from_loader(countries_file):
    field = FishingTrip._meta.get_field("country_code")

    assert list(field.choices) == [("PL", "Poland"), ("AT", "Austria")]


def test_model_country_name_property():
    assert FishingTrip(country_code="PL").country_name == "Poland"
    assert FishingTrip(country_code="ZZ").country_name == "ZZ"