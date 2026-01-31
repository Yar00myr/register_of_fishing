from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views

from .views import (
    homepage_view,
    logout_page,
    add_trip_view,
    trips_list_view,
    trip_detail_view,
    delete_trip,
    new_fish_type,
    edit_trip,
)


app_name = "api"


urlpatterns = [
    path("", homepage_view, name="homepage"),
    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="api/login.html", success_url=reverse_lazy("api:homepage")
        ),
        name="login",
    ),
    path("logout/", logout_page, name="logout"),
    path("trips/add/", add_trip_view, name="fishingtrip-add"),
    path("trips/", trips_list_view, name="fishingtrip-list"),
    path("trips<int:pk>/", trip_detail_view, name="fishingtrip-detail"),
    path("trips/<int:pk>/edit", edit_trip, name="fishingtrip-edit"),
    path("trips/<int:pk>/delete/", delete_trip, name="fishingtrip-delete"),
    path("fish/add/", new_fish_type, name="new_fish_type"),
]
