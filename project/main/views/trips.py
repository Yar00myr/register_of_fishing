from dataclasses import dataclass

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from ..forms import CatchFormSet, CatchPhotoFormSet, FishingTripForm
from ..models import Catch, FishingTrip
from ..selectors import get_trip_catch_summary


@dataclass(frozen=True)
class SortOption:
    label: str
    order_by: str
    opposite: str


SORT_OPTIONS: dict[str, SortOption] = {
    "-date": SortOption("Date ↓", "-date", opposite="date"),
    "date": SortOption("Date ↑", "date", opposite="-date"),
    "country": SortOption("Country A→Z", "country_code", opposite="-country"),
    "-country": SortOption("Country Z→A", "-country_code", opposite="country"),
}
DEFAULT_SORT = "-date"


class TripListView(LoginRequiredMixin, ListView):
    model = FishingTrip
    template_name = "main/fishing_list.html"
    context_object_name = "trips"

    def get_sort(self) -> str:
        key = self.request.GET.get("sort", DEFAULT_SORT)
        return key if key in SORT_OPTIONS else DEFAULT_SORT

    def get_queryset(self):
        return super().get_queryset().order_by(SORT_OPTIONS[self.get_sort()].order_by)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current = self.get_sort()
        context["sort_buttons"] = [
            {
                "label": option.label,
                "active": key == current,
                "target": option.opposite if key == current else key,
            }
            for key, option in SORT_OPTIONS.items()
        ]
        return context


class TripDetailView(LoginRequiredMixin, DetailView):
    template_name = "main/fishing_detail.html"
    context_object_name = "trip"
    queryset = FishingTrip.objects.prefetch_related(
        "catches__fish_type", "catches__photos"
    )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["catch_summary"] = get_trip_catch_summary(self.object)
        return context


class TripDeleteView(LoginRequiredMixin, DeleteView):
    model = FishingTrip
    success_url = reverse_lazy("main:fishingtrip-list")
    http_method_names = ["post"]

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'Trip "{self.object}" deleted.')
        return response


class TripFormMixin(LoginRequiredMixin):
    

    model = FishingTrip
    form_class = FishingTripForm
    template_name = "main/fishing_form.html"
    success_message = ""
    is_edit = False

    def get_formset(self):
        kwargs = {"instance": self.object, "prefix": "form"}
        if self.request.method == "POST":
            kwargs.update(data=self.request.POST, files=self.request.FILES)
        return CatchFormSet(**kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.setdefault("formset", self.get_formset())
        context["is_edit"] = self.is_edit
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object() if self.is_edit else None
        form = self.get_form()
        formset = self.get_formset()
        if form.is_valid() and formset.is_valid():
            return self.forms_valid(form, formset)
        return self.render_to_response(
            self.get_context_data(form=form, formset=formset)
        )

    @transaction.atomic
    def forms_valid(self, form, formset):
        self.object = form.save()
        formset.instance = self.object
        formset.save()
        messages.success(self.request, self.success_message)
        return redirect(self.get_success_url())


class TripCreateView(TripFormMixin, CreateView):
    success_message = "Trip added successfully!"

    def get_success_url(self):
        return reverse("main:fishingtrip-list")


class TripUpdateView(TripFormMixin, UpdateView):
    success_message = "Trip updated successfully!"
    is_edit = True

    def get_success_url(self):
        return reverse("main:fishingtrip-detail", kwargs={"pk": self.object.pk})


@login_required
def catch_photos_view(request, pk: int):
    catch = get_object_or_404(
        Catch.objects.select_related("fishing_trip", "fish_type").prefetch_related(
            "photos"
        ),
        pk=pk,
    )
    if request.method == "POST":
        formset = CatchPhotoFormSet(request.POST, request.FILES, instance=catch)
        if formset.is_valid():
            formset.save()
            messages.success(request, "Photos saved!")
            return redirect("main:fishingtrip-detail", pk=catch.fishing_trip_id)
    else:
        formset = CatchPhotoFormSet(instance=catch)

    return render(
        request, "main/catch_photos.html", {"catch": catch, "formset": formset}
    )
