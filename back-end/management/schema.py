import graphene

from affix.queries import Query as AffixQuery
from ingredients.queries import Query as IngredientQuery
from recipe_designs.queries import Query as RecipeDesignQuery
from menus.queries import Query as MenuQuery

from affix.mutations import Mutation as AffixMutation
from ingredients.mutations import Mutation as IngredientMutation
from recipe_designs.mutations import Mutation as RecipeDesignMutation
from menus.mutations import Mutation as MenuMutation


class Query(AffixQuery, IngredientQuery, RecipeDesignQuery, MenuQuery, graphene.ObjectType):
    pass


class Mutation(AffixMutation, IngredientMutation, RecipeDesignMutation, MenuMutation, graphene.ObjectType):
    pass
