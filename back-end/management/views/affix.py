from rest_framework import generics
from rest_framework.permissions import AllowAny

from management.models.affix import Alergen, Attribute, Diet, KitchenAccesory
from management.serializers.affix import AlergenSerializer, AttributeSerializer, DietSerializer, KitchenSerializer

from utils.models import Unit
from utils.serializers import UnitSerializer


class UnitListAPI(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer


class AttributeListAPI(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = Attribute.objects.all()
    serializer_class = AttributeSerializer


class AlergenListAPI(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = Alergen.objects.all()
    serializer_class = AlergenSerializer


class DietListAPI(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = Diet.objects.all()
    serializer_class = DietSerializer


class KitchenListAPI(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = KitchenAccesory.objects.all()
    serializer_class = KitchenSerializer
