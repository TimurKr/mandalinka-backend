from rest_framework import serializers

from management.models.ingredients import Ingredient


class ListIngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = (
            'id',
            'name',
            'img',
            'is_active',
            'is_inactive',
            'is_deleted',
            'status',
            'cost',
            'unit',
            'usage_last_month',
        )


class DetailIngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'
