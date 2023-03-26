import graphene

from graphene_django.types import DjangoObjectType

from management.graphql.types.recipe_designs import (
    RecipeDesignType,
)

from management.models.recipe_designs import (
    RecipeDesign,
)


class Query(graphene.ObjectType):
    recipe_designs = graphene.List(RecipeDesignType)
    recipe_design_by_id = graphene.Field(RecipeDesignType, id=graphene.Int())

    def resolve_recipe_designs(self, info, **kwargs):
        return RecipeDesign.objects.all()

    def resolve_recipe_design_by_id(self, info, id):
        return RecipeDesign.objects.get(id=id)
