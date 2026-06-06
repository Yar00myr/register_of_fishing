from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Count, Sum
from django.shortcuts import redirect, render, get_object_or_404
from django.views.decorators.http import require_POST

from ..forms import FishTypeForm, CatchPhotoFormSet
from ..models import FishingTrip, FishType, Catch


def login_page(request):
    if request.user.is_authenticated:
        return redirect("main:homepage")

    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            login(request, form.get_user())
            return redirect("main:homepage")

    return render(request, "main/login.html", {"form": form})


@require_POST
def logout_page(request):
    logout(request)
    return redirect("main:login")


@login_required(login_url="main:login")
def homepage_view(request):
    fish_types = FishType.objects.order_by("name")
    fish_type_form = FishTypeForm()
    stats = FishingTrip.total_stats()

    trips_by_country = dict(
        FishingTrip.objects.values("country_code")
        .annotate(count=Count("id"))
        .values_list("country_code", "count")
    )
    fish_by_country = dict(
        FishingTrip.objects.values("country_code")
        .annotate(total=Count("catches"))
        .values_list("country_code", "total")
    )

    top_catches = (
        Catch.objects.filter(photos__isnull=False)
        .prefetch_related("photos")
        .order_by("-weight")
        .distinct()[:3]
    )

    context = {
        "fish_types": fish_types,
        "fish_type_form": fish_type_form,
        "total_fish": stats["total_fish"],
        "total_weight": stats["total_weight"],
        "trips_by_country": trips_by_country,
        "fish_by_country": fish_by_country,
        "total_trips_count": FishingTrip.objects.count(),
        "top_catches": top_catches,
    }
    return render(request, "main/homepage.html", context=context)


@login_required(login_url="main:login")
@require_POST
def new_fish_type(request):
    form = FishTypeForm(request.POST)
    if form.is_valid():
        form.save()
        messages.success(request, "Fish type added successfully!")
    else:
        messages.error(request, "Failed to add fish type. Please check the form.")
    return redirect("main:homepage")


# @login_required(login_url="api:login")
# def catch_detail_view(request, pk: int):
#     catch = get_object_or_404(Catch.objects.prefetch_related("photos"), pk=pk)
#     if request.method == "POST":
#         formset = CatchPhotoFormSet(request.POST, request.FILES, instance=catch)
#         if formset.is_valid():
#             formset.save()
#             messages.success(request, "Photos saved!")
#             return redirect("api:catch-detail", pk=catch.pk)
#     else:
#         formset = CatchPhotoFormSet(instance=catch)

#     return render(
#         request,
#         "api/catch_detail.html",
#         {
#             "catch": catch,
#             "formset": formset,
#         },
#     )
