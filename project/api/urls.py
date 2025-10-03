from django.urls import path, include

from rest_framework import routers

from .views import (
    FishingTripViewSet,
    FishTypeViewSet,
    LoginView,
    CatchViewSet,
    LogoutView,
    homepage_view,
    login_page,
    logout_page,
    add_trip_view,
    trips_list_view,
    trip_detail_view,
)


app_name = "api"

router = routers.SimpleRouter()
router.register(r"fishingtrip", FishingTripViewSet, basename="fishingtrip")
router.register(r"fishtype", FishTypeViewSet, basename="fishtype")
router.register(r"catch", CatchViewSet, basename="catch")



urlpatterns = [
    path("api/auth/login/", LoginView.as_view(), name="api-login"),
    path("api/auth/logout/", LogoutView.as_view(), name="api-logout"),
    path("api/", include(router.urls)),
    path("", homepage_view, name="homepage"),
    path("login/", login_page, name="login"),
    path("logout/", logout_page, name="logout"),
    path("trips/add/", add_trip_view, name="fishingtrip-add"),
    path("trips/", trips_list_view, name="fishingtrip-list"),
    path("trips<int:pk>/", trip_detail_view, name="fishingtrip-detail"),
]
