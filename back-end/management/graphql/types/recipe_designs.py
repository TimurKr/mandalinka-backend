import graphene

from graphene_django.types import DjangoObjectType

from utils.schema import StatusTypeMixin, TimeStampTypeMixin
from management.models.recipe_designs import (
    RecipeDesign,
    RDIngredient,
    RDStep,
    RDError,
)


class RDErrorType(StatusTypeMixin, DjangoObjectType):
    class Meta:
        model = RDError
        fields = (
            'id',
            'code',
            'message'
        )


class RecipeDesignType(StatusTypeMixin, TimeStampTypeMixin, DjangoObjectType):
    class Meta:
        model = RecipeDesign
        fields = (
            # General
            'id',
            'name',
            'description',
            'thumbnail',
            'predecessor',
            'successor',
            'exclusive_inheritance',
            'price',
            # Cooking related
            'difficulty',
            'cooking_time',
            'active_cooking_time',
            'attributes',
            'diet',
            'required_accessories',
            # Publishing checklists
            'description_finished',
            'steps_finished',
            'ingredients_finished',
            'todo',

            # Relations
            'ingredients',
            'steps',

            'created_by',
        )

    cost = graphene.Float()
    version = graphene.Int()
    errors = graphene.List(RDErrorType)

    def resolve_cost(self, info, **kwargs):
        return self.cost

    def resolve_version_number(self, info, **kwargs):
        return self.version

    def resolve_errors(self, info, **kwargs):
        return self._automatic_errors


class RDIngredientType(StatusTypeMixin, TimeStampTypeMixin, DjangoObjectType):
    class Meta:
        model = RDIngredient
        fields = (
            'id',
            'ingredient',
            'recipe',
            'amount',
            'unit',
            'alternative_for',
        )

    cost = graphene.Float()

    def resolve_cost(self, info, **kwargs):
        return self.cost


class RDStepType(StatusTypeMixin, TimeStampTypeMixin, DjangoObjectType):
    class Meta:
        model = RDStep
        fields = (
            'id',
            'recipe',
            'number',
            'text',
            'thumbnail',
        )
