from rest_framework import generics, mixins
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from management.models.ingredients import Ingredient
from management.serializers.ingredients import ListIngredientSerializer, DetailIngredientSerializer


class IngredientListCreate(generics.ListCreateAPIView):
    """
    Class based view for Ingredient API
    Provides the following methods:
        GET - returns all ingredients
        POST - creates new ingredient
    """
    queryset = Ingredient.objects.all()
    serializer_class = ListIngredientSerializer


class IngredientDetail(generics.RetrieveUpdateAPIView):
    """
    Class based view for Ingredient API
    Provides the following methods:
        GET - returns ingredient with given id
        PUT - updates ingredient with given id (only inactive ingredients can be updated)
    """
    queryset = Ingredient.objects.all()
    serializer_class = DetailIngredientSerializer
