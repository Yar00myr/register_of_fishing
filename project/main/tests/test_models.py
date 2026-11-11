import pytest
from decimal import Decimal
from datetime import date
from main.models import FishingTrip, FishType, Catch, CatchPhoto


class TestFishType:
    def test_create(self, db):
        ft = FishType.objects.create(name="Perch")
        assert ft.name == "Perch"

    def test_str(self, fish_type):
        assert str(fish_type) == "Carp"

    def test_unique_name(self, db, fish_type):
        from django.db import IntegrityError

        with pytest.raises(IntegrityError):
            FishType.objects.create(name="Carp")

    def test_ordering(self, db):
        FishType.objects.create(name="Pike")
        FishType.objects.create(name="Perch")
        FishType.objects.create(name="Carp")
        names = list(FishType.objects.values_list("name", flat=True))
        assert names == sorted(names)


class TestFishingTrip:
    def test_create(self, trip):
        assert trip.name == "Summer fishing"
        assert trip.country_code == "UA"

    def test_str_with_name(self, trip):
        assert str(trip) == f"Fishing trip — Summer fishing ({trip.date})"

    def test_str_without_name(self, db):
        trip = FishingTrip.objects.create(
            name="",
            country_code="UA",
            date=date(2024, 6, 15),
        )
        assert str(trip) == f"Fishing trip — Ukraine ({trip.date})"

    def test_country_name(self, trip):
        assert trip.country_name == "Ukraine"

    def test_country_name_unknown_code(self, db):
        trip = FishingTrip.objects.create(country_code="XX", date=date(2024, 1, 1))
        assert trip.country_name == "XX"


class TestCatch:
    def test_create(self, catch):
        assert catch.weight == Decimal("1.50")

    def test_str_with_weight(self, catch):
        assert str(catch) == "Carp (1.50 kg)"

    def test_str_without_weight(self, db, trip, fish_type):
        catch = Catch.objects.create(
            fishing_trip=trip, fish_type=fish_type, weight=None
        )
        assert str(catch) == "Carp"


class TestCatchPhoto:
    def test_create(self, db, catch):
        photo = CatchPhoto.objects.create(
            catch=catch,
            photo="catches/1/test.jpg",
            caption="Test photo",
        )
        assert photo.caption == "Test photo"
        assert photo.catch == catch

    def test_default_caption(self, db, catch):
        photo = CatchPhoto.objects.create(catch=catch, photo="catches/1/test.jpg")
        assert photo.caption == ""
