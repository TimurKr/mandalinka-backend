from django.forms import ValidationError
from rest_framework import generics, mixins, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import AllowAny

from management.models.ingredients import Ingredient, IngredientVersion
from management.serializers.ingredients import ListIngredientSerializer, IngredientDetailSerializer, IngredientVersionSerializer

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
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        try:
            response = super().post(
                request, *args, **kwargs)
        except Exception as e:
            print(e)
            raise e

        return response


class IngredientDetailAPI(generics.RetrieveUpdateAPIView):
    """
    Class based view for Ingredient API
    Provides the following methods:
        GET - returns ingredient with given id
        PUT - updates ingredient with given id (only inactive ingredients can be updated)
        PATCH - updates ingredient with given id (only inactive ingredients can be updated)
        DELETE - soft deletes ingredient with given id (only inactive ingredients can be deleted)
    """
    permission_classes = [AllowAny]
    queryset = Ingredient.objects.all()
    serializer_class = IngredientDetailSerializer

    def patch(self, request, *args, **kwargs):

        ingredient = self.get_object()

        if request.data.get('status', False):
            new_status = request.data.get('status', False)
            if new_status == 'deleted':
                ingredient.soft_delete()
            elif new_status == 'inactive':
                ingredient.deactivate()
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST, data={'message': 'Invalid status.'})
            serializer = self.get_serializer(ingredient)
            return Response(serializer.data)

        return super().patch(request, *args, **kwargs)

    # def delete(self, request, *args, **kwargs):
    #     ingredient = self.get_object()
    #     ingredient.soft_delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)


class IngredientVersionCreateAPI(generics.CreateAPIView):
    """
    Class based view for IngredientVersion API
    Provides the following methods:
        POST - creates new version of ingredient
    """
    permission_classes = [AllowAny]
    queryset = IngredientVersion.objects.all()
    serializer_class = IngredientVersionSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        unit = request.data.get('unit', False)

        # Call serializer.save() instead of super().create()
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class IngredientVersionModifyAPI(generics.RetrieveUpdateAPIView):
    """
    Class based view for IngredientVersion API
    Provides the following methods:
        GET - returns ingredient version with given id

    """
    permission_classes = [AllowAny]
    queryset = IngredientVersion.objects.all()
    serializer_class = IngredientVersionSerializer

    def patch(self, request, *args, **kwargs):
        ingredient_version = self.get_object()
        serializer = self.get_serializer(ingredient_version)

        new_status = request.data.get('status')
        if new_status:
            try:
                if new_status == 'active':
                    ingredient_version.activate()
                elif new_status == 'deleted':
                    ingredient_version.soft_delete()
                elif new_status == 'inactive':
                    ingredient_version.deactivate()
                else:
                    return Response(status=status.HTTP_400_BAD_REQUEST, data={'message': 'Invalid status.'})
            except Exception as e:
                return Response(status=status.HTTP_400_BAD_REQUEST, data={'message': e.message})
            return Response(serializer.data)

        return Response(serializer.data)
        # return super().patch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
