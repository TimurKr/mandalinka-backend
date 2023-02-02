from rest_framework import serializers
from .models import Unit


class StatusSerializer(serializers.ModelSerializer):
    status = serializers.CharField(read_only=True)
    active = serializers.BooleanField(read_only=True)
    inactive = serializers.BooleanField(read_only=True)
    deleted = serializers.BooleanField(read_only=True)


class BaseUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = '__all__'


class UnitSerializer(serializers.ModelSerializer):
    base_unit = BaseUnitSerializer(read_only=True)

    class Meta:
        model = Unit
        fields = '__all__'
        depth = 1
