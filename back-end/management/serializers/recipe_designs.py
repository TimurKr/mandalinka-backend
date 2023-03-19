from management.models.ingredients import IngredientVersionStockOrder
from utils.models import Unit
from rest_framework import serializers


from management.models.recipe_designs import RecipeDesign, RDStep, RDIngredient
from utils.serializers import UnitSerializer


class RDStepSerializer(serializers.ModelSerializer):
    """
    Serializer for listing and creating recipe design steps
    """

    class Meta:
        model = RDStep
        fields = (
            'id',
            'recipe',
            'number',
            'text',
            'thumbnail',
        )
        read_only_fields = (
            'id',
        )


class RDIngredientSerializer(serializers.ModelSerializer):
    """
    Serializer for listing and creating recipe design ingredients
    """
    unit = UnitSerializer()

    class Meta:
        model = RDIngredient
        fields = (
            'id',
            'recipe',
            'ingredient',
            'alternative_for',
            'unit',
            'amount',
            'text',
            'cost',
        )
        read_only_fields = (
            'id',
            'cost',
        )
        depth = 1


class RecipeDesignListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing recipe designs
    """
    url = serializers.URLField(source='get_absolute_url', required=False)

    class Meta:
        model = RecipeDesign
        fields = (
            'id',
            'name',
            'description',
            'thumbnail',
            'predecessor',
            'successor',
            'url',
            'is_active',
            'is_inactive',
            'is_deleted',
        )
        read_only_fields = (
            'id',
            'name',
            'description',
            'thumbnail',
            'predecessor',
            'successor',
            'is_active',
            'is_inactive',
            'is_deleted',
        )


class RecipeDesignCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating new recipe designs
    """

    steps = RDStepSerializer(many=True, required=False)
    ingredients = RDIngredientSerializer(many=True, required=False)

    class Meta:
        model = RecipeDesign
        fields = (
            'id',
            'name',
            'description',
            'thumbnail',
            'predecessor',
            'exclusive_inheritance',
            'steps',
            'ingredients',
            'difficulty',
            'cooking_time',
            'active_cooking_time',
            'attributes',
            'diet',
            'required_accessories',
            'description_finished',
            'steps_finished',
            'ingredients_finished',
            'todo',
            'price',
        )
        read_only_fields = (
            'id',
        )

    def create(self, validated_data):
        steps_data = validated_data.pop('steps', None)
        recipe = RecipeDesign.objects.create(**validated_data)
        if steps_data is not None:
            for step_data in steps_data:
                RDStep.objects.create(recipe=recipe, **step_data)
        return recipe
