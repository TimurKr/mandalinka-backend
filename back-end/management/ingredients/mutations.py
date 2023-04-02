import graphene
from graphene_file_upload.scalars import Upload

from graphene_django.forms.mutation import DjangoModelFormMutation
from .forms import IngredientForm

from .models import (
    Ingredient,
)

from .types import (
    IngredientType,
)


class IngredientMutation(DjangoModelFormMutation):
    ingredient = graphene.Field(IngredientType)

    class Meta:
        form_class = IngredientForm
        model = Ingredient
        file_fields = {
            'img': {
                'required': False,
                'type': Upload,
            }
        }


class Mutation(graphene.ObjectType):
    create_ingredient = IngredientMutation.Field()
    update_ingredient = IngredientMutation.Field()
    delete_ingredient = IngredientMutation.Field()
