import graphene
from graphene_django import DjangoObjectType

from .models import Attribute, Alergen, Diet, KitchenAccesory


class AttributeType(DjangoObjectType):
    class Meta:
        model = Attribute
        fields = (
            'id',
            'name',
            'icon',
        )


class AlergenType(DjangoObjectType):
    class Meta:
        model = Alergen
        fields = (
            'name',
            'code',
        )


class DietType(DjangoObjectType):
    class Meta:
        model = Diet
        fields = (
            'id',
            'name',
            'icon',
        )


class KitchenAccesoryType(DjangoObjectType):
    class Meta:
        model = KitchenAccesory
        fields = (
            'id',
            'name',
            'icon',
        )
