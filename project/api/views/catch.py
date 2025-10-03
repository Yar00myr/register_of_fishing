from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from ..models import Catch
from ..serializers import CatchSerializer


class CatchViewSet(ModelViewSet):
    queryset = Catch.objects.all()
    serializer_class = CatchSerializer
    permission_classes = [IsAuthenticated]
