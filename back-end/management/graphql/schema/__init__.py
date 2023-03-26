import graphene

from .affix import Query as AffixQuery
from .ingredients import (
    Query as IngredientsQuery,
    Mutation as IngredientsMutation
)
from .recipe_designs import Query as RecipeDesignsQuery


class Query(
        AffixQuery,
        IngredientsQuery,
        RecipeDesignsQuery,
        graphene.ObjectType):
    pass


class Mutation(
        IngredientsMutation,
        graphene.ObjectType):
    pass
