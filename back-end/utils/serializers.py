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


class UnitField(serializers.PrimaryKeyRelatedField):
    """Custom field for accepting both a Unit instance and a primary key"""
    queryset = Unit.objects.all()

    def to_representation(self, value):
        """Return the primary key of the Unit instance"""
        return value.pk if value else None

    def to_internal_value(self, data):
        """Return the Unit instance corresponding to the primary key"""
        try:
            return Unit.objects.get(pk=data)
        except Unit.DoesNotExist:
            self.fail('does_not_exist', pk_value=data)


class UnitSerializer(serializers.ModelSerializer):
    base_unit = BaseUnitSerializer(read_only=True)

    class Meta:
        model = Unit
        fields = '__all__'
        depth = 2
