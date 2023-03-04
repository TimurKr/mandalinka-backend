from rest_framework import serializers

from management.models.affix import Alergen


class AlergenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alergen
        fields = (
            'code',
            'name',
        )
