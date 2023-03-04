from rest_framework import generics, mixins, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import AllowAny

from management.models.ingredients import Ingredient
from management.serializers.ingredients import ListIngredientSerializer, IngredientDetailSerializer

from management.models.affix import Alergen
from management.serializers.affix import AlergenSerializer

from utils.models import Unit
from utils.serializers import UnitSerializer


class IngredientListCreateAPI(generics.ListCreateAPIView):
    """
    Class based view for Ingredient API
    Provides the following methods:
        GET - returns all ingredients
        POST - creates new ingredient
    """
    permission_classes = [AllowAny]
    queryset = Ingredient.objects.all()
    serializer_class = ListIngredientSerializer

    parser_classes = [MultiPartParser]

    def get(self, request, *args, **kwargs):
        return super(IngredientListCreateAPI, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        try:
            response = super(IngredientListCreateAPI, self).post(
                request, *args, **kwargs)
        except Exception as e:
            print(e)
            raise e

        print

        return response


class IngredientDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    """
    Class based view for Ingredient API
    Provides the following methods:
        GET - returns ingredient with given id
        PUT - updates ingredient with given id (only inactive ingredients can be updated)
    """
    permission_classes = [AllowAny]
    queryset = Ingredient.objects.all()
    serializer_class = IngredientDetailSerializer

    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
