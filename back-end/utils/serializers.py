from rest_framework import serializers
from .models import Unit


class StatusSerializer(serializers.ModelSerializer):
    status = serializers.CharField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)
    is_inactive = serializers.BooleanField(read_only=True)
    is_deleted = serializers.BooleanField(read_only=True)


class BaseUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = [
            'id',
            'name',
            'sign',
        ]


class UnitSerializer(serializers.ModelSerializer):
    base_unit = BaseUnitSerializer(read_only=True)

    class Meta:
        model = Unit
        fields = '__all__'
        depth = 1
