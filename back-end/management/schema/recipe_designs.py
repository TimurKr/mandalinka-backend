import graphene

from graphene_django.types import DjangoObjectType

from utils.schema import StatusTypeMixin, TimeStampTypeMixin
from management.models.recipe_designs import (
    RecipeDesign,
    RDIngredient,
    RDStep,
    RDError,
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
    errors = graphene.List('management.schema.recipe_designs.RDErrorType')

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


class RDErrorType(StatusTypeMixin, DjangoObjectType):
    class Meta:
        model = RDError
        fields = (
            'id',
            'code',
            'message'
        )


class Query(graphene.ObjectType):
    recipe_designs = graphene.List(RecipeDesignType)
    recipe_design_by_id = graphene.Field(RecipeDesignType, id=graphene.Int())

    def resolve_recipe_designs(self, info, **kwargs):
        return RecipeDesign.objects.all()

    def resolve_recipe_design_by_id(self, info, id):
        return RecipeDesign.objects.get(id=id)
