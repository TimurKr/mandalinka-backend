from management.models.ingredients import IngredientVersionStockOrder
from utils.models import Unit
from rest_framework import serializers


from management.models.ingredients import Ingredient, IngredientVersion, IngredientVersionStockChange, IngredientVersionStockOrder, IngredientVersionStockRemove
from utils.serializers import UnitSerializer


class IngredientVersionStockChangeSerializer(serializers.ModelSerializer):
    """Serializer for listing ingredient stock changes and creating new instances"""
    unit = UnitSerializer(read_only=True)
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
            'ingredient_version',
            'amount',
            'unit',
        )

    def create(self, validated_data):
        raise serializers.ValidationError(
            'Creation not allowed for this endpoint.')

    def update(self, instance, validated_data):
        raise serializers.ValidationError(
            'Updating not allowed for this endpoint.')


class IngredientVersionStockRemoveSerializer(serializers.ModelSerializer):
    """Serialer for creating stock changes for removing ingredients"""
    unit = serializers.PrimaryKeyRelatedField(
        queryset=Unit.objects.all(), required=False)

    class Meta:
        model = IngredientVersionStockRemove
        fields = (
            'id',
            'ingredient_version',
            'amount',
            'unit',
            'reason',
            'description',
            'date',
        )
        read_only_fields = (
            'id',
        )

    def validate(self, data):
        """Check if unit is valid property for the ingredient_version"""

        if data.get('unit'):
            if data['unit'].property != data['ingredient_version'].unit.property:
                allowed_units = []
                for unit in Unit.objects.all():
                    if unit.property == data['ingredient_version'].unit.property:
                        allowed_units.append(unit.sign)
                raise serializers.ValidationError(
                    f'Jednotky sa nezhodujú. Zvolte jednu z {", ".join(allowed_units)}')

        return super().validate(data)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['unit'] = UnitSerializer(instance.unit).data
        return data


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
            'expiration_date',
            'is_expired',
            'cost',
            'in_stock_amount'
        )
        read_only_fields = (
            'id',
            'in_stock_amount',
        )

    def validate(self, data: dict):
        """
        - Check if unit is valid property for the ingredient_version
        - Check if delivery_date is after order_date
        - Check if expiration_date is after delivery_date
        """

        if data.get('unit'):
            if data['unit'].property != data['ingredient_version'].unit.property:
                allowed_units = []
                for unit in Unit.objects.all():
                    if unit.property == data['ingredient_version'].unit.property:
                        allowed_units.append(unit.sign)
                raise serializers.ValidationError(
                    f'Jednotky sa nezhodujú. Zvolte jednu z {", ".join(allowed_units)}')

        if data.get('delivery_date') and data.get('order_date'):
            if data['delivery_date'] < data['order_date']:
                raise serializers.ValidationError(
                    'Dátum dodania musí byť po dátume objednania.')

        if data.get('expiration_date') and data.get('delivery_date'):
            if data['expiration_date'] <= data['delivery_date'].date():
                raise serializers.ValidationError(
                    'Dátum expirácie musí byť po dátume dodania.')

        if self.instance:
            if not data.get('is_delivered', self.instance.is_delivered) and data.get('is_expired', self.instance.is_expired):
                raise serializers.ValidationError(
                    'Nedoručená objednávka nemôže byť expirovaná.')
        else:
            if not data.get('is_delivered', False) and data.get('is_expired', False):
                raise serializers.ValidationError(
                    'Nedoručená objednávka nemôže byť expirovaná.')

        return super().validate(data)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['unit'] = UnitSerializer(instance.unit).data
        return data


class IngredientVersionSerializer(serializers.ModelSerializer):
    """Serializer for listing ingredient versions and creating new instances"""
    url = serializers.URLField(source='get_absolute_url', required=False)
    unit = serializers.PrimaryKeyRelatedField(
        queryset=Unit.objects.all(), required=False)
    stock_changes = IngredientVersionStockChangeSerializer(
        many=True, read_only=True)
    orders = IngredientVersionStockOrderSerializer(many=True, read_only=True)
    removals = IngredientVersionStockRemoveSerializer(
        many=True, read_only=True)

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
            'source',
            'expiration_period',
            'in_stock_amount',
            'stock_changes',
            'orders',
            'removals',
        )
        read_only_fields = (
            'id',
            'version_number',
            'cost',
            'url',
            'unit',
            'is_active',
            'is_inactive',
            'is_deleted',
            'in_stock_amount',
            'stock_changes',
            'orders',
        )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['unit'] = UnitSerializer(instance.unit).data
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
    unit = UnitSerializer(read_only=True)

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
