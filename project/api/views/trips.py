from collections import defaultdict
from decimal import Decimal


from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404

from ..forms import FishingTripForm, CatchFormSet
from ..models import FishingTrip


@login_required(login_url="api:login")
def add_trip_view(request):
    if request.method == "POST":
        trip_form = FishingTripForm(request.POST)
        formset = CatchFormSet(request.POST, request.FILES, prefix="form")
        if trip_form.is_valid() and formset.is_valid():
            trip = trip_form.save()
            formset.instance = trip
            formset.save()
            return redirect("api:fishingtrip-list")
    else:
        trip_form = FishingTripForm()
        formset = CatchFormSet(prefix="form")

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
def trip_detail_view(request, pk: int):
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
def delete_trip(request, pk: int):
    trip = get_object_or_404(FishingTrip, id=pk)
    if request.method == "POST":
        trip.delete()
        return redirect("api:fishingtrip-list")
    else:

        return render(request, "api/delete_trip.html", {"trip": trip})


@login_required(login_url="api:login")
def edit_trip(request, pk: int):
    trip = get_object_or_404(FishingTrip, id=pk)
    if request.method == "POST":
        form = FishingTripForm(request.POST, instance=trip)
        formset = CatchFormSet(
            request.POST, request.FILES, instance=trip, prefix="form"
        )
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect("api:fishingtrip-detail", pk=trip.pk)
    else:
        form = FishingTripForm(instance=trip)
        formset = CatchFormSet(instance=trip, prefix="form")

    return render(
        request,
        "api/fishing_form.html",
        {
            "form": form,
            "formset": formset,
            "trip": trip,
            "is_edit": True,
        },
    )
