from django import forms

from management.models.ingredients import Ingredient


class IngredientForm(forms.ModelForm):

    class Meta:
        model = Ingredient
        fields = ('name','extra_info','img','alergens','unit')
