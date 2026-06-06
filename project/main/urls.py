from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views

from .views import (
    login_page,
    logout_page,
    homepage_view,
    add_trip_view,
    trips_list_view,
    trip_detail_view,
    delete_trip,
    new_fish_type,
    edit_trip,
)

app_name = "main"


urlpatterns = [
    path("", homepage_view, name="homepage"),
    path("login/", login_page, name="login"),
    path("logout/", logout_page, name="logout"),
    path("trips/add/", add_trip_view, name="fishingtrip-add"),
    path("trips/", trips_list_view, name="fishingtrip-list"),
    path("trips<int:pk>/", trip_detail_view, name="fishingtrip-detail"),
    path("trips/<int:pk>/edit", edit_trip, name="fishingtrip-edit"),
    path("trips/<int:pk>/delete/", delete_trip, name="fishingtrip-delete"),
    path("fish/add/", new_fish_type, name="new_fish_type"),
]
