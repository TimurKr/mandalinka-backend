from rest_framework import serializers
from rest_framework.fields import URLField

from management.models.ingredients import Ingredient, IngredientVersion


class ListIngredientSerializer(serializers.ModelSerializer):
    url = serializers.URLField(source='get_absolute_url', required=False)

    class Meta:
        model = Ingredient
        fields = (
            'id',
            'name',
            'unit',
            'alergens',
            'img',
            'usage_last_month',
            'url',
            'is_active',
            'is_inactive',
            'is_deleted',
        )


class IngredientVersionSerializer(serializers.ModelSerializer):
    url = serializers.URLField(source='get_absolute_url')

    class Meta:
        model = IngredientVersion
        fields = (
            'version_number',
            'url',
            'is_active',
            'is_inactive',
            'is_deleted',

        )


class IngredientDetailSerializer(serializers.ModelSerializer):
    versions = IngredientVersionSerializer(many=True, read_only=True)

    class Meta:
        model = Ingredient
        fields = (
            'id',
            'name',
            'unit',
            'alergens',
            'img',
            'status',
            'cost',
            'usage_last_month',
            'versions',
        )
