import graphene

from graphene_django import DjangoObjectType

from utils.schema import TimeStampTypeMixin, StatusTypeMixin
from .models import (
    Ingredient,
    IngredientVersion,
)


class IngredientType(
        StatusTypeMixin,
        DjangoObjectType):

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
    usage_last_month = graphene.Float()
    url = graphene.String()

    def resolve_in_stock_amount(self, info, **kwargs):
        return self.in_stock_amount

    def resolve_usage_last_month(self, info, **kwargs):
        return self.usage_last_month

    def resolve_url(self, info, **kwargs):
        return self.get_absolute_url


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
