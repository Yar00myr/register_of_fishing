import pytest

from datetime import date
from decimal import Decimal

from django.contrib.auth import get_user_model

from main.models import Catch, FishingTrip, FishType


@pytest.fixture(autouse=True)
def override_staticfiles(settings):
    """Templates use {% static %}, but collectstatic is not run in tests."""
    settings.STORAGES = {
        "default": {
            "BACKEND": "django.core.files.storage.FileSystemStorage",
        },
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
        },
    }


@pytest.fixture(autouse=True)
def fast_password_hasher(settings):
    """MD5 is insecure but ~100x faster than PBKDF2, which is fine for tests."""
    settings.PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]


@pytest.fixture
def user(db):
    return get_user_model().objects.create_user(
        username="testuser", password="testpass"
    )


@pytest.fixture
def auth_client(client, user):
    client.force_login(user)
    return client


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
