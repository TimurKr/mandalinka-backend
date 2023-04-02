import graphene

from .models import Attribute, Alergen, Diet, KitchenAccesory

from .types import (
    AttributeType,
    AlergenType,
    DietType,
    KitchenAccesoryType,
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
