from rest_framework import serializers
from .models import Ingredient, IngredientVersion
from .forms import IngredientVersionForm
from utils.serializers import UnitSerializer, StatusSerializer
from django.template.loader import render_to_string


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

    new_version_form = serializers.SerializerMethodField()

    class Meta:
        model = Ingredient
        fields = '__all__'
        depth = 1

    def get_new_version_form(self, obj):
        new_version_form = render_to_string(
            "ingredients/forms/form.html", {'form': IngredientVersionForm(obj)}, request=self.context.get('request')
        )
        return new_version_form


class IngredientVersionSerializer(serializers.ModelSerializer):
    ingredient = serializers.StringRelatedField(read_only=True)
    in_stock = serializers.IntegerField(read_only=True)
    unit = UnitSerializer(read_only=True)
    version_number = serializers.IntegerField(read_only=True)
    status = serializers.CharField(read_only=True)
    active = serializers.BooleanField(read_only=True)
    inactive = serializers.BooleanField(read_only=True)
    deleted = serializers.BooleanField(read_only=True)

    edit_form = serializers.SerializerMethodField()

    class Meta:
        model = IngredientVersion
        fields = '__all__'
        depth = 1
        extra_kwargs = {'edit_ingredient_form': {'read_only': True}}

    def get_edit_form(self, obj):
        edit_form = render_to_string(
            "ingredients/forms/form.html", {'form': IngredientVersionForm(obj)}, request=self.context.get('request')
        )
        return edit_form
