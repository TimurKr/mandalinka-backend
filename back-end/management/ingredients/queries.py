import graphene
from graphene_file_upload.scalars import Upload

from graphene_django.forms.mutation import DjangoModelFormMutation
from .forms import IngredientForm

from .models import (
    Ingredient,
    IngredientVersion,
)

from .types import (
    IngredientType,
    IngredientVersionType,
)


class IngredientQuery(graphene.ObjectType):
    ingredients = graphene.List(IngredientType)
    ingredient_by_id = graphene.Field(IngredientType, id=graphene.Int())

    def resolve_ingredients(self, info, **kwargs):
        return Ingredient.objects.all()

    def resolve_ingredient_by_id(self, info, id):
        return Ingredient.objects.get(id=id)


class IngredientVersionQuery(graphene.ObjectType):
    ingredient_versions = graphene.List(IngredientVersionType)
    ingredient_version_by_id = graphene.Field(
        IngredientVersionType, id=graphene.Int())

    def resolve_ingredient_versions(self, info, **kwargs):
        return IngredientVersion.objects.all()

    def resolve_ingredient_version_by_id(self, info, id):
        return IngredientVersion.objects.get(id=id)


class Query(IngredientQuery, IngredientVersionQuery, graphene.ObjectType):
    pass
