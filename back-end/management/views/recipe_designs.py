from django.forms import ValidationError
from rest_framework import generics, mixins, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import AllowAny

from management.models.recipe_designs import RecipeDesign

from management.serializers.recipe_designs import RecipeDesignListSerializer, RecipeDesignCreateSerializer


class RecipeDesignListCreateAPI(generics.ListCreateAPIView):
    """
    View for listing and creating recipe designs
    """
    queryset = RecipeDesign.objects.all()
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipeDesignListSerializer
        elif self.request.method == 'POST':
            return RecipeDesignCreateSerializer
