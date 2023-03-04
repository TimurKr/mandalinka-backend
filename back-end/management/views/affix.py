from rest_framework import generics
from rest_framework.permissions import AllowAny

from management.models.affix import Alergen
from management.serializers.affix import AlergenSerializer

from utils.models import Unit
from utils.serializers import BaseUnitSerializer


class AlergenListAPI(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = Alergen.objects.all()
    serializer_class = AlergenSerializer


class UnitListAPI(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = Unit.objects.all()
    serializer_class = BaseUnitSerializer
