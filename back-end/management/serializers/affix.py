from rest_framework import serializers

from management.models.affix import Alergen, Attribute, Diet, KitchenAccesory


class AttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attribute
        fields = (
            'id',
            'name',
            'icon',
        )
        read_only_fields = (
            'id',
            'name',
            'icon',
        )


class AlergenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alergen
        fields = (
            'code',
            'name',
        )
        read_only_fields = (
            'code',
            'name',
        )


class DietSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diet
        fields = (
            'id',
            'name',
            'icon',
        )
        read_only_fields = (
            'id',
            'name',
            'icon',
        )


class KitchenSerializer(serializers.ModelSerializer):
    class Meta:
        model = KitchenAccesory
        fields = (
            'id',
            'name',
            'icon',
        )
        read_only_fields = (
            'id',
            'name',
            'icon',
        )
