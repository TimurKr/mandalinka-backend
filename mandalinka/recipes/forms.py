from django import forms

from .models import Recipe, Ingredient, IngredientInstance

from django.core.exceptions import ValidationError

from django.urls import reverse, reverse_lazy
from django.urls.exceptions import NoReverseMatch
from django.utils.translation import gettext_lazy as _

from django.contrib.admin.forms import *

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, HTML, BaseInput, Field
from crispy_forms.bootstrap import StrictButton
from crispy_bootstrap5.bootstrap5 import FloatingField


class SubmitButton(BaseInput):
    input_type = 'submit'
    field_classes = 'btn primary-button'

class SecondarySubmitButton(BaseInput):
    input_type = 'submit'
    field_classes = 'btn secondary-button'

class SecondaryButton(StrictButton):
    field_classes = 'btn secondary-button'

    def __init__(self, content, onclick = None, *args, **kwargs):
        if onclick:
            onclick = f'location.href="{reverse(onclick)}"'
            super().__init__(content, onclick=onclick, *args, **kwargs)
        else:
            super().__init__(content, *args, **kwargs)


# RECIPES #######################################################################

class RecipeForm(forms.ModelForm):

    step1 = forms.CharField(max_length=128,
        label='Krok 1',
        help_text='Kroky sa zdedia iba v prípade, ak budú všetky "-"',
        initial="-", strip=True,
        required=False,
    )
    step2 = forms.CharField(max_length=128,
        label='Krok 2', 
        initial="-", strip=True,
        required=False,
    )
    step3 = forms.CharField(max_length=128,
        label='Krok 3', 
        initial="-", strip=True, 
        required=False,
    )
    step4 = forms.CharField(max_length=128,
        label='Krok 4', 
        initial="-", strip=True,
        required=False,
    )
    step5 = forms.CharField(max_length=128,
        label='Krok 5', 
        initial="-", strip=True,
        required=False,
    )
    step6 = forms.CharField(max_length=128,
        label='Krok 6', 
        initial="-", strip=True,
        required=False,
    )

    steps_fields = (step1, step2, step3, step4, step5, step6)



    class Meta:
        model = Recipe
        fields = (
            'predecessor',
            'exclusive_predecessor',
            'name',
            'description',
            'thumbnail',
            'steps',
            'difficulty',
            'StF_cooking_time', 
            'active_cooking_time',
            'attributes',
            'diet',
            'created_by',
        )
        widgets = {
            'diet': forms.CheckboxSelectMultiple(),
            'attributes': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['predecessor'].help_text += '. V každom poli kde zadáte "-" sa automaticky zdedia hodnoty z predchodcu.'

        self.helper = FormHelper(self)
        self.helper.form_id = 'general_info'
        self.helper.form_class = 'needs-validation'
        self.helper.attrs = {'novalidate': ''}
        self.helper.layout = Layout(
            'predecessor',
            'exclusive_predecessor',
            'name',
            'description',
            'thumbnail',
            'step1',
            'step2',
            'step3',
            'step4',
            'step5',
            'step6',
            'difficulty',
            'StF_cooking_time', 
            'active_cooking_time',
            'attributes',
            'diet',
            'created_by',
            SubmitButton('Submit', 'Vytvoriť'),
        )

    def save(self, commit=True):
        super().save(commit=commit)
        print("saved")
        if self.predecessor:
            print("Budeme dediť")
        else:
            print("Nebudeme dediť")

        steps = ''
        for step in self.steps_fields:
            steps += step
            steps += '\n'
        steps.strip()
        self.steps = steps

class NewRecipeForm(RecipeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.form_action = reverse_lazy('recipes:add_recipe')


class IngredientInstanceForm(forms.ModelForm):
    class Meta:
        model = IngredientInstance
        fields = ('ingredient', 'amount')
        widgets = {
            'ingredient': forms.Select(),
        }


IngredientInstanceFormset = forms.inlineformset_factory(Recipe, IngredientInstance, 
    form=IngredientInstanceForm, 
    )
    
        

# INGREDIENTS #######################################################################

class IngredientForm(forms.ModelForm):

    class Meta:
        model = Ingredient
        fields = (
            'name', 
            'img', 
            'unit',
            'price_per_unit',
            'alergens',
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
            'price_per_unit',
            'alergens',
            Div(
                Div(SecondarySubmitButton('submit', 'Uložiť'), css_class='col-sm-6'),
                Div(SubmitButton('submit', 'Uložiť a aktivovať'), css_class='col-sm-6'),
                css_class='row g-2'
            )
        )

class NewIngredientForm(IngredientForm):
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.form_action = reverse_lazy('recipes:add_ingredient')

class EditIngredientForm(NewIngredientForm):
    def __init__(self, ingredient_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.form_action = reverse_lazy('recipes:edit_ingredient', args=(ingredient_id))