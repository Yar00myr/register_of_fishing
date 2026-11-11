from django.urls import path

from . import views

app_name = "main"


urlpatterns = [
    path("", views.homepage_view, name="homepage"),
    path("login/", views.login_page, name="login"),
    path("logout/", views.logout_page, name="logout"),
    path("catches/<int:pk>/photos/", views.catch_photos_view, name="catch-photos"),
    path("trips/add/", views.TripCreateView.as_view(), name="fishingtrip-add"),
    path("trips/", views.TripListView.as_view(), name="fishingtrip-list"),
    path("trips<int:pk>/", views.TripDetailView.as_view(), name="fishingtrip-detail"),
    path(
        "trips/<int:pk>/edit", views.TripUpdateView.as_view(), name="fishingtrip-edit"
    ),
    path(
        "trips/<int:pk>/delete/",
        views.TripDeleteView.as_view(),
        name="fishingtrip-delete",
    ),
    path("fish/add/", views.new_fish_type, name="new_fish_type"),
]
