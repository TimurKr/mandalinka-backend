import graphene

from graphene_django.types import DjangoObjectType

from utils.schema import StatusTypeMixin
from management.models.ingredients import (
    Ingredient,
    IngredientVersion,
    IngredientVersionStockChange,
    IngredientVersionStockRemove,
    IngredientVersionStockOrder
)


class IngredientType(DjangoObjectType):

    class Meta:
        model = Ingredient
        fields = (
            'id',
            'name',
            'extra_info',
            'img',
            'alergens',
            'unit',
            'versions',
        )

    in_stock_amount = graphene.Float()

    def resolve_in_stock_amount(self, info, **kwargs):
        return self.in_stock_amount


class IngredientVersionType(StatusTypeMixin, DjangoObjectType):
    class Meta:
        model = IngredientVersion
        fields = (
            'id',
            'ingredient',
            'source',
            'expiration_period',
        )

    version_number = graphene.Int()
    cost = graphene.Float()
    in_stock_amount = graphene.Float()

    def resolve_version_number(self, info, **kwargs):
        return self.version_number

    def resolve_cost(self, info, **kwargs):
        return self.cost

    def resolve_in_stock_amount(self, info, **kwargs):
        return self.in_stock_amount


class Query(graphene.ObjectType):
    ingredients = graphene.List(IngredientType)
    ingredient_by_id = graphene.Field(IngredientType, id=graphene.Int())

    def resolve_ingredients(self, info, **kwargs):
        return Ingredient.objects.all()

    def resolve_ingredient_by_id(self, info, id):
        return Ingredient.objects.get(id=id)

    ingredient_versions = graphene.List(IngredientVersionType)
    ingredient_version_by_id = graphene.Field(
        IngredientVersionType, id=graphene.Int())

    def resolve_ingredient_versions(self, info, **kwargs):
        return IngredientVersion.objects.all()

    def resolve_ingredient_version_by_id(self, info, id):
        return IngredientVersion.objects.get(id=id)
