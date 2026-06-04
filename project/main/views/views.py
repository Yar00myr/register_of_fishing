from collections import defaultdict
from decimal import Decimal

from django.contrib import messages
from django.views.decorators.http import require_POST
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404

from ..forms import FishingTripForm, CatchFormSet, FishTypeForm
from ..models import FishingTrip, FishType, Catch


def login_page(request):
    return render(request, "api/login.html")


def logout_page(request):
    if request.method == "POST":
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
@require_POST
def new_fish_type(request):
    form = FishTypeForm(request.POST)
    if form.is_valid():
        form.save()
        messages.success(request, "Fish type added successfully!")
    else:
        messages.error(request, form.errors.as_text())

    return redirect("api:homepage")
