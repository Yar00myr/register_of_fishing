from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from ..forms import FishTypeForm
from ..models import FishType
from ..selectors import get_country_stats, get_overall_stats, get_top_catches


def login_page(request):
    if request.user.is_authenticated:
        return redirect("main:homepage")

    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        login(request, form.get_user())
        return redirect("main:homepage")

    return render(request, "main/login.html", {"form": form})


@require_POST
def logout_page(request):
    logout(request)
    return redirect("main:login")


@login_required
def homepage_view(request):
    context = {
        "fish_types": FishType.objects.all(), 
        "fish_type_form": FishTypeForm(),
        "stats": get_overall_stats(),
        "country_stats": get_country_stats(),
        "top_catches": get_top_catches(),
    }
    return render(request, "main/homepage.html", context)


@login_required
@require_POST
def new_fish_type(request):
    form = FishTypeForm(request.POST)
    if form.is_valid():
        form.save()
        messages.success(request, "Fish type added successfully!")
    else:
        messages.error(request, "Failed to add fish type. Please check the form.")
    return redirect("main:homepage")