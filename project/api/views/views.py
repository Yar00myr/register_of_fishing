from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404

from ..forms import FishingTripForm, CatchFormSet, FishTypeForm
from ..models import FishingTrip, FishType


def login_page(request):
    return render(request, "api/login.html")


def logout_page(request):
    logout(request)
    return redirect("api:login")


@login_required(login_url="api:login")
def homepage_view(request):
    fish_types = FishType.objects.all()
    fish_type_form = FishTypeForm()
    return render(
        request,
        "api/_base.html",
        {"fish_types": fish_types, "fish_type_form": fish_type_form},
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
    trips = FishingTrip.objects.all().prefetch_related("catches")
    return render(request, "api/fishing_list.html", {"trips": trips})


@login_required(login_url="api:login")
def trip_detail_view(request, pk):
    trip = get_object_or_404(FishingTrip.objects.prefetch_related("catches"), pk=pk)
    return render(request, "api/fishing_detail.html", {"trip": trip})


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
