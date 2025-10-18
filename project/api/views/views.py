from collections import defaultdict
from decimal import Decimal

from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404

from ..forms import FishingTripForm, CatchFormSet, FishTypeForm
from ..models import FishingTrip, FishType, Catch


def login_page(request):
    return render(request, "api/login.html")


def logout_page(request):
    logout(request)
    return redirect("api:login")


@login_required(login_url="api:login")
def homepage_view(request):
    fish_types = FishType.objects.all()
    fishing_trips = FishingTrip.objects.all()
    fish_type_form = FishTypeForm()
    stats = FishingTrip.total_stats()
    total_trips_count = FishingTrip.objects.count()

    trips_by_country = {}
    for trip in fishing_trips:
        country = trip.country_code
        trips_by_country[country] = trips_by_country.get(country, 0) + 1

    fish_by_country = {}
    for trip in fishing_trips:
        country = trip.country_code
        total_catch = sum(getattr(catch, "quantity", 1) for catch in trip.catches.all())
        fish_by_country[country] = fish_by_country.get(country, 0) + total_catch

    top_catches = Catch.objects.filter(photo__isnull=False).order_by("-weight")[:3]

    context = {
        "fish_types": fish_types,
        "fish_type_form": fish_type_form,
        "total_fish": stats["total_fish"],
        "total_weight": stats["total_weight"],
        "trips_by_country": trips_by_country,
        "fish_by_country": fish_by_country,
        "total_trips_count": total_trips_count,
        "top_catches": top_catches,
    }
    return render(
        request,
        "api/homepage.html",
        context=context,
    )


@login_required(login_url="api:login")
def add_trip_view(request):
    if request.method == "POST":
        trip_form = FishingTripForm(request.POST)
        formset = CatchFormSet(request.POST, request.FILES)
        if trip_form.is_valid() and formset.is_valid():
            trip = trip_form.save()
            formset.instance = trip
            formset.save()
            return redirect("api:fishingtrip-list")
    else:
        trip_form = FishingTripForm()
        formset = CatchFormSet()

    return render(
        request,
        "api/fishing_form.html",
        {
            "form": trip_form,
            "formset": formset,
        },
    )


@login_required(login_url="api:login")
def trips_list_view(request):
    trips = FishingTrip.objects.all().prefetch_related("catches").order_by("date")
    return render(request, "api/fishing_list.html", {"trips": trips})


@login_required(login_url="api:login")
def trip_detail_view(request, pk):
    trip = get_object_or_404(FishingTrip.objects.prefetch_related("catches"), pk=pk)

    grouped = defaultdict(
        lambda: {
            "total_amount": 0,
            "total_weight": Decimal("0"),
            "weights": list(),
        }
    )

    for catch in trip.catches.all():
        name = catch.fish_type.name
        grouped[name]["total_amount"] += catch.amount
        grouped[name]["total_weight"] += catch.total_weight
        if catch.weight:
            grouped[name]["weights"].append(catch.weight)

    grouped_catches = []
    for name, data in grouped.items():
        grouped_catches.append(
            {
                "fish_type": name,
                "amount": data["total_amount"],
                "weights": sorted(data["weights"]),
                "total_weight": data["total_weight"],
            }
        )

    return render(
        request,
        "api/fishing_detail.html",
        {"trip": trip, "grouped_catches": grouped_catches},
    )


@login_required(login_url="api:login")
@require_POST
def new_fish_type(request):
    form = FishTypeForm(request.POST)
    if form.is_valid():
        fish = form.save()
        return JsonResponse(
            {
                "success": True,
                "name": fish.name,
                "id": fish.id,
                "message": f"Fish type '{fish.name}' added successfully!",
            }
        )
    else:
        return JsonResponse({"success": False, "errors": form.errors}, status=400)
