from collections import defaultdict
from decimal import Decimal

from django.db.models import Count, F, Prefetch, QuerySet, Sum

from .models import Catch, CatchPhoto, FishingTrip

ZERO = Decimal(0)
_FISH_NAME = "fish_type__name"


def get_overall_stats() -> dict:
    """Trips, fish and total weight across all trips in a single query."""
    return FishingTrip.objects.aggregate(
        total_trips=Count("id", distinct=True),
        total_fish=Count("catches"),
        total_weight=Sum("catches__weight", default=ZERO),
    )


def get_country_stats() -> list[dict]:
    """Trips and fish per country in a single query."""
    return list(
        FishingTrip.objects.values("country_code")
        .annotate(trips=Count("id", distinct=True), fish=Count("catches"))
        .order_by("country_code")
    )


def get_top_catches(limit: int = 3) -> QuerySet[Catch]:
    """Heaviest catches that have at least one photo."""
    return (
        Catch.objects.filter(photos__isnull=False)
        .select_related("fish_type")
        .prefetch_related(
            Prefetch("photos", queryset=CatchPhoto.objects.order_by("uploaded_at"))
        )
        .order_by("-weight")
        .distinct()[:limit]
    )


def get_trip_catch_summary(trip: FishingTrip) -> dict:
    """Per-fish-type rows and grand totals for one trip.

    ``amount`` and ``total_weight`` are aggregated by the database. The list of
    individual weights cannot be (portably) aggregated, so it is a second query.
    """
    rows = list(
        trip.catches.values(name=F(_FISH_NAME))
        .annotate(amount=Count("id"), total_weight=Sum("weight", default=ZERO))
        .order_by("name")
    )

    weights = defaultdict(list)
    for name, weight in (
        trip.catches.filter(weight__isnull=False)
        .order_by("weight")
        .values_list(_FISH_NAME, "weight")
    ):
        weights[name].append(weight)

    for row in rows:
        row["fish_type"] = row.pop("name")
        row["weights"] = weights[row["fish_type"]]

    return {
        "rows": rows,
        "total_amount": sum(r["amount"] for r in rows),
        "total_weight": sum((r["total_weight"] for r in rows), ZERO),
    }
