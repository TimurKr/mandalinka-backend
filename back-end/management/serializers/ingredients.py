from management.models.ingredients import IngredientVersionStockOrder
from utils.models import Unit
from rest_framework import serializers
from rest_framework.fields import URLField

from management.models.ingredients import Ingredient, IngredientVersion, IngredientVersionStockChange, IngredientVersionStockOrder
from utils.serializers import UnitSerializer


class IngredientVersionStockChangeSerializer(serializers.ModelSerializer):
    """Serializer for listing ingredient stock changes and creating new instances"""
    unit = serializers.PrimaryKeyRelatedField(
        queryset=Unit.objects.all(), required=False)
    ingredient_version = serializers.PrimaryKeyRelatedField(
        queryset=IngredientVersion.objects.all(), required=False)

    class Meta:
        model = IngredientVersionStockChange
        fields = (
            'id',
            'ingredient_version',
            'amount',
            'unit'
        )
        read_only_fields = (
            'id',
            'ingredient_version'
        )

    def create(self, validated_data):
        raise serializers.ValidationError(
            'Creation not allowed for this endpoint.')

    def update(self, instance, validated_data):
        raise serializers.ValidationError(
            'Updating not allowed for this endpoint.')


class IngredientVersionStockOrderSerializer(serializers.ModelSerializer):
    """
    Serializer for listing the orders of IngredientVersions
    """
    unit = serializers.PrimaryKeyRelatedField(
        queryset=Unit.objects.all(), required=False)
    ingredient_version = serializers.PrimaryKeyRelatedField(
        queryset=IngredientVersion.objects.all(), required=False)

    class Meta:
        model = IngredientVersionStockOrder
        fields = (
            'id',
            'ingredient_version',
            'amount',
            'unit',
            'description',
            'order_date',
            'delivery_date',
            'is_delivered',
        )
        read_only_fields = (
            'id',
            'is_delivered',
        )


class IngredientVersionSerializer(serializers.ModelSerializer):
    """Serializer for listing ingredient versions and creating new instances"""
    url = serializers.URLField(source='get_absolute_url', required=False)
    amount = serializers.FloatField(required=False)
    unit = serializers.PrimaryKeyRelatedField(
        queryset=Unit.objects.all(), required=False)
    stock_changes = IngredientVersionStockChangeSerializer(
        many=True, read_only=True)
    orders = IngredientVersionStockOrderSerializer(many=True, read_only=True)

    class Meta:
        model = IngredientVersion
        fields = (
            'id',
            'ingredient',
            'version_number',
            'cost',
            'url',
            'is_active',
            'is_inactive',
            'is_deleted',
            'unit',
            'amount',
            'source',
            'in_stock_amount',
            'stock_changes',
            'orders',
        )
        read_only_fields = (
            'id',
            'version_number',
            'url',
            'is_active',
            'is_inactive',
            'is_deleted',
            'unit',
            'amount',
            'in_stock_amount',
            'stock_changes',
            'orders',
        )

    def validate(self, data):
        """If unit has been provided, convert the amount to the correct unit """
        if 'unit' not in data or 'amount' not in data:
            raise serializers.ValidationError(
                'If you want to create a new IngredientVersion, you must provide the unit and the amount for the given cost.')

        if data['unit'].property != data['ingredient'].unit.property:
            allowed_units = []
            for unit in Unit.objects.all():
                if unit.property == data['ingredient'].unit.property:
                    allowed_units.append(unit.sign)
            raise serializers.ValidationError(
                f'Jednotky sa nezhodujú. Zvolte jednu z {", ".join(allowed_units)}')

        data['cost'] = data['cost'] / data['ingredient'].unit.from_base(
            data['unit'].to_base(data['amount']))

        data.pop('unit')
        data.pop('amount')

        return data


class ListIngredientSerializer(serializers.ModelSerializer):
    """Serializer for listing ingredients and creating new instances"""
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
        read_only_fields = (
            'id',
            'usage_last_month',
            'url',
            'is_active',
            'is_inactive',
            'is_deleted',
        )


class IngredientDetailSerializer(serializers.ModelSerializer):
    """Serializer for retrieving and updating ingredients"""
    versions = IngredientVersionSerializer(many=True, read_only=True)

    class Meta:
        model = Ingredient
        fields = (
            'id',
            'name',
            'extra_info',
            'unit',
            'alergens',
            'status',
            'is_active',
            'is_inactive',
            'is_deleted',
            'img',
            'cost',
            'usage_last_month',
            'in_stock_amount',
            'versions',
        )
        read_only_fields = (
            'id',
            'status',
            'usage_last_month',
            'versions',
            'is_active',
            'is_inactive',
            'is_deleted',
            'in_stock_amount',
        )
