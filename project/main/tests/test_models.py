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

    def test_total_weight_no_catches(self, trip):
        assert trip.total_weight == Decimal("0")

    def test_total_weight_with_catches(self, trip, fish_type):
        Catch.objects.create(
            fishing_trip=trip, fish_type=fish_type, weight=Decimal("1.00")
        )
        Catch.objects.create(
            fishing_trip=trip, fish_type=fish_type, weight=Decimal("2.50")
        )
        assert trip.total_weight == Decimal("3.50")

    def test_total_fish_amount(self, trip, fish_type):
        Catch.objects.create(
            fishing_trip=trip, fish_type=fish_type, weight=Decimal("1.00")
        )
        Catch.objects.create(
            fishing_trip=trip, fish_type=fish_type, weight=Decimal("2.00")
        )
        assert trip.total_fish_amount == 2

    def test_total_stats(self, trip, fish_type):
        Catch.objects.create(
            fishing_trip=trip, fish_type=fish_type, weight=Decimal("1.00")
        )
        Catch.objects.create(
            fishing_trip=trip, fish_type=fish_type, weight=Decimal("2.00")
        )
        stats = FishingTrip.total_stats()
        assert stats["total_fish"] == 2
        assert stats["total_weight"] == Decimal("3.00")

    def test_total_stats_empty(self, db):
        stats = FishingTrip.total_stats()
        assert stats["total_fish"] == 0
        assert stats["total_weight"] == Decimal("0")

    def test_grouped_catches(self, trip, fish_type, fish_type_2):
        Catch.objects.create(
            fishing_trip=trip, fish_type=fish_type, weight=Decimal("1.00")
        )
        Catch.objects.create(
            fishing_trip=trip, fish_type=fish_type, weight=Decimal("2.00")
        )
        Catch.objects.create(
            fishing_trip=trip, fish_type=fish_type_2, weight=Decimal("3.00")
        )
        grouped = trip.grouped_catches()
        names = [g["fish_type"] for g in grouped]
        assert "Carp" in names
        assert "Pike" in names
        data = next(g for g in grouped if g["fish_type"] == "Carp")
        assert data["amount"] == 2
        assert data["total_weight"] == Decimal("3.00")
        assert data["weights"] == [Decimal("1.00"), Decimal("2.00")]


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

    def test_total_weight_with_value(self, catch):
        assert catch.total_weight == Decimal("1.50")

    def test_total_weight_none(self, db, trip, fish_type):
        catch = Catch.objects.create(
            fishing_trip=trip, fish_type=fish_type, weight=None
        )
        assert catch.total_weight == Decimal("0")


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
