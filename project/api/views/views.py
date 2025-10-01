from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404

from ..forms import FishingTripForm, CatchFormSet
from ..models import FishingTrip


def login_page(request):
    return render(request, "api/login.html")


def logout_page(request):
    logout(request)
    return redirect("api:login")


@login_required(login_url="api:login")
def homepage_view(request):
    return render(request, "api/_base.html")


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
    trips = FishingTrip.objects.all().prefetch_related("catches")
    return render(request, "api/fishing_list.html", {"trips": trips})


@login_required(login_url="api:login")
def trip_detail_view(request, pk):
    trip = get_object_or_404(FishingTrip.objects.prefetch_related("catches"), pk=pk)
    return render(request, "api/fishing_detail.html", {"trip": trip})
