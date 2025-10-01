import logging

from rest_framework import filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from ..serializers import FishingTripSerializer
from ..models import FishingTrip

logger = logging.getLogger("api")


class FishingTripViewSet(ModelViewSet):
    queryset = FishingTrip.objects.all().prefetch_related("catches")
    serializer_class = FishingTripSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["country_code"]
    ordering_fields = ["date"]

    def perform_create(self, serializer):
        instance = serializer.save()
        logger.info(
            f"[CREATE] User={self.request.user.username} "
            f"created FishingTrip id={instance.id}, date={instance.date}, country={instance.country_code}"
        )
        return instance

    def perform_update(self, serializer):
        instance = serializer.save()
        logger.info(
            f"[UPDATE] User={self.request.user.username} "
            f"updated FishingTrip id={instance.id}, date={instance.date}, country={instance.country_code}"
        )
        return instance

    def perform_destroy(self, instance):
        logger.info(
            f"[DELETE] User={self.request.user.username} "
            f"deleted FishingTrip id={instance.id}, date={instance.date}, country={instance.country_code}"
        )
        super().perform_destroy(instance)
