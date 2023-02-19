from rest_framework import serializers
from rest_framework.fields import URLField

from management.models.ingredients import Ingredient, IngredientVersion


class ListIngredientSerializer(serializers.ModelSerializer):
    url = serializers.URLField(source='get_absolute_url')

    class Meta:
        model = Ingredient
        fields = (
            'id',
            'name',
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


class DetailIngredientSerializer(serializers.ModelSerializer):
    versions = IngredientVersionSerializer(many=True, read_only=True)

    class Meta:
        model = Ingredient
        fields = (
            'id',
            'name',
            'unit',
            'cost',
            'usage_last_month',
            'versions',
        )
