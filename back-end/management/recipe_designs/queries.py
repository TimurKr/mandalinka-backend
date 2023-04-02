import graphene

from .types import (
    RecipeDesignType,
)

from .models import (
    RecipeDesign,
)


class Query(graphene.ObjectType):
    recipe_designs = graphene.List(RecipeDesignType)
    recipe_design_by_id = graphene.Field(RecipeDesignType, id=graphene.Int())

    def resolve_recipe_designs(self, info, **kwargs):
        return RecipeDesign.objects.all()

    def resolve_recipe_design_by_id(self, info, id):
        return RecipeDesign.objects.get(id=id)
