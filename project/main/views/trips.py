from collections import defaultdict
from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404

from ..forms import FishingTripForm, CatchFormSet, CatchPhotoFormSet
from ..models import FishingTrip, Catch


@login_required(login_url="main:login")
def add_trip_view(request):
    if request.method == "POST":
        form = FishingTripForm(request.POST)
        formset = CatchFormSet(request.POST, request.FILES, prefix="form")
        if form.is_valid() and formset.is_valid():
            trip = form.save()
            formset.instance = trip
            formset.save()
            messages.success(request, "Trip added successfully!")
            return redirect("main:fishingtrip-list")
    else:
        form = FishingTripForm()
        formset = CatchFormSet(prefix="form")

    return render(
        request,
        "main/fishing_form.html",
        {
            "form": form,
            "formset": formset,
        },
    )


@login_required(login_url="main:login")
def trips_list_view(request):
    sort = request.GET.get("sort", "-date")

    allowed_sorts = {
        "-date": "-date",
        "date": "date",
        "country": "country_code",
        "-country": "-country_code",
    }
    order_by = allowed_sorts.get(sort, "-date")

    trips = FishingTrip.objects.prefetch_related("catches").order_by(order_by)
    return render(
        request, "main/fishing_list.html", {"trips": trips, "current_sort": sort}
    )


@login_required(login_url="main:login")
def trip_detail_view(request, pk: int):
    trip = get_object_or_404(
        FishingTrip.objects.prefetch_related("catches__fish_type", "catches__photos"),
        pk=pk,
    )
    return render(
        request,
        "main/fishing_detail.html",
        {
            "trip": trip,
            "grouped_catches": trip.grouped_catches(),
        },
    )


@login_required(login_url="main:login")
def delete_trip(request, pk: int):
    trip = get_object_or_404(FishingTrip, pk=pk)
    if request.method == "POST":
        trip.delete()
        messages.success(request, f'Trip "{trip}" deleted.')
        return redirect("main:fishingtrip-list")
    return render(request, "main/delete_trip.html", {"trip": trip})


@login_required(login_url="main:login")
def edit_trip(request, pk: int):
    trip = get_object_or_404(FishingTrip, pk=pk)
    if request.method == "POST":
        form = FishingTripForm(request.POST, instance=trip)
        formset = CatchFormSet(
            request.POST,
            request.FILES,
            instance=trip,
            prefix="form",
        )
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, "Trip updated successfully!")
            return redirect("main:fishingtrip-detail", pk=trip.pk)
    else:
        form = FishingTripForm(instance=trip)
        formset = CatchFormSet(instance=trip, prefix="form")

    return render(
        request,
        "main/fishing_form.html",
        {
            "form": form,
            "formset": formset,
            "trip": trip,
            "is_edit": True,
        },
    )


@login_required(login_url="main:login")
def catch_photos_view(request, pk: int):
    catch = get_object_or_404(Catch.objects.prefetch_related("photos"), pk=pk)
    if request.method == "POST":
        formset = CatchPhotoFormSet(request.POST, request.FILES, instance=catch)
        if formset.is_valid():
            formset.save()
            messages.success(request, "Photos saved!")
            return redirect("main:fishingtrip-detail", pk=catch.fishing_trip_id)
    else:
        formset = CatchPhotoFormSet(instance=catch)

    return render(
        request,
        "main/catch_photos.html",
        {
            "catch": catch,
            "formset": formset,
        },
    )
