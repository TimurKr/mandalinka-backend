import graphene
from graphene_django import DjangoObjectType

from management.models.affix import Attribute, Alergen, Diet, KitchenAccesory


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


class Query(graphene.ObjectType):
    attributes = graphene.List(AttributeType)
    alergens = graphene.List(AlergenType)
    diets = graphene.List(DietType)
    kitchen_accesories = graphene.List(KitchenAccesoryType)

    def resolve_attributes(self, info, **kwargs):
        return Attribute.objects.all()

    def resolve_alergens(self, info, **kwargs):
        return Alergen.objects.all()

    def resolve_diets(self, info, **kwargs):
        return Diet.objects.all()

    def resolve_kitchen_accesories(self, info, **kwargs):
        return KitchenAccesory.objects.all()
