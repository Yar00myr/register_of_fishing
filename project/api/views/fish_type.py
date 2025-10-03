from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from ..models import FishType
from ..serializers import FishTypeSerializer


class FishTypeViewSet(ModelViewSet):
    queryset = FishType.objects.all()
    serializer_class = FishTypeSerializer
    permission_classes = [IsAuthenticated]
