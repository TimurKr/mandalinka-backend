from rest_framework import serializers
from .models import Ingredient, IngredientVersion
from utils.serializers import UnitSerializer, StatusSerializer


class BasicIngredientVersionSerializer(serializers.ModelSerializer):
    ingredient = serializers.SlugRelatedField(
        read_only=True, slug_field='name')

    class Meta:
        model = IngredientVersion
        fields = ('id', 'version_number', 'status', 'ingredient')


class IngredientSerializer(serializers.ModelSerializer):
    is_active = serializers.BooleanField(read_only=True)
    status = serializers.CharField(read_only=True)
    cost = serializers.FloatField(read_only=True)
    usage_last_month = serializers.IntegerField(read_only=True)
    unit = UnitSerializer(read_only=True)
    versions = BasicIngredientVersionSerializer(many=True, read_only=True)

    class Meta:
        model = Ingredient
        fields = '__all__'
        depth = 1


class IngredientVersionSerializer(serializers.ModelSerializer):
    ingredient = serializers.StringRelatedField(read_only=True)
    in_stock = serializers.IntegerField(read_only=True)
    unit = UnitSerializer(read_only=True)
    version_number = serializers.IntegerField(read_only=True)
    status = serializers.CharField(read_only=True)
    active = serializers.BooleanField(read_only=True)
    inactive = serializers.BooleanField(read_only=True)
    deleted = serializers.BooleanField(read_only=True)
    # status_changed = serializers.DateTimeField(
    #     format="%d %B, %H:%M:%S", read_only=True)

    class Meta:
        model = IngredientVersion
        fields = '__all__'
        depth = 1
