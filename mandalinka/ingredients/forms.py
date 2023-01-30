from django import forms
from django.urls import reverse_lazy

from .models import Ingredient, IngredientVersion

from utils.forms import SubmitButton, SecondarySubmitButton
from utils.models import Unit
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div

class IngredientForm(forms.ModelForm):

    class Meta:
        model = Ingredient
        fields = (
            'name', 
            'img', 
            'alergens',
            'unit',
        )
        widgets = {
            'alergens': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_class = 'needs-validation'
        self.helper.attrs = {'novalidate': ''}
        self.helper.layout = Layout(
            'name', 
            'img', 
            'unit',
            'alergens',
            Div(
                Div(SubmitButton('submit', 'Vytvoriť'), css_class='col-sm-6 ms-auto'),
                css_class='row g-2'
            )
        )

class NewIngredientForm(IngredientForm):
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.form_action = reverse_lazy('ingredients:add')


class NewIngredientVersionForm(forms.ModelForm):

    amount = forms.IntegerField(label="Množstvo", min_value=1, required=True, initial=1)
    unit = forms.ModelChoiceField(queryset=Unit.objects.all(), label="Jednotka", required=True)

    class Meta:
        model = IngredientVersion
        fields = (
            'ingredient', 
            'cost', 
            'source',
        )

    def __init__(self, ingredient: Ingredient, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['ingredient'].initial = ingredient
        self.fields['ingredient'].disabled = True
        self.fields['ingredient'].queryset = Ingredient.objects.filter(pk=ingredient.pk)

        self.fields['unit'].initial = ingredient.unit
        self.fields['unit'].queryset = Unit.objects.filter(property=ingredient.unit.property)

        self.fields['cost'].help_text = 'Zadajte cenu pre zvolené množstvo zvolenej jednotky'

        self.helper = FormHelper(self)
        self.helper.form_class = 'needs-validation'
        self.helper.form_tag = False
        self.helper.attrs = {'novalidate': ''}
        self.helper.layout = Layout(
            'ingredient',
            Div(
                Div('amount', css_class='col-sm-8 mb-2'),
                Div('unit', css_class='col-sm-4'),
                css_class='row g-2'
            ),
            'cost', 
            'source', 
            Div(
                Div(SubmitButton('submit', 'Vytvoriť'), css_class='col-sm-6 ms-auto'),
                css_class='row g-2'
            )
        )