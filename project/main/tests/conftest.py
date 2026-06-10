import pytest

from decimal import Decimal
from datetime import date
from django.contrib.auth.models import User

from main.models import FishingTrip, FishType, Catch


@pytest.fixture
def user(db):
    return User.objects.create_user(username="testuser", password="testpass")


@pytest.fixture
def auth_client(client, user):
    client.login(username="testuser", password="testpass")
    return client

@pytest.fixture(autouse=True)
def override_staticfiles(settings):
    settings.STORAGES = {
        "default": {
            "BACKEND": "django.core.files.storage.FileSystemStorage",
        },
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
        },
    }

@pytest.fixture
def fish_type(db):
    return FishType.objects.create(name="Carp")


@pytest.fixture
def fish_type_2(db):
    return FishType.objects.create(name="Pike")


@pytest.fixture
def trip(db):
    return FishingTrip.objects.create(
        name="Summer fishing",
        country_code="UA",
        date=date(2024, 6, 15),
    )


@pytest.fixture
def catch(db, trip, fish_type):
    return Catch.objects.create(
        fishing_trip=trip,
        fish_type=fish_type,
        weight=Decimal("1.50"),
    )
