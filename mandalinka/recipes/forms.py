from django import forms

from .models import Recipe

from django.core.exceptions import ValidationError

from django.urls import reverse, reverse_lazy
from django.urls.exceptions import NoReverseMatch
from django.utils.translation import gettext_lazy as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, HTML, BaseInput, Field
from crispy_forms.bootstrap import StrictButton
from crispy_bootstrap5.bootstrap5 import FloatingField


class SubmitButton(BaseInput):
    input_type = 'submit'
    field_classes = 'btn primary-button'

class SecondaryButton(StrictButton):
    field_classes = 'btn secondary-button'

    def __init__(self, content, onclick = None, *args, **kwargs):
        if onclick:
            onclick = f'location.href="{reverse(onclick)}"'
            super().__init__(content, onclick=onclick, *args, **kwargs)
        else:
            super().__init__(content, *args, **kwargs)


class IngredientForm(forms.ModelForm):

    class Meta:
        model = Recipe
        fields = ('__all__')

# RECIPES #######################################################################

class NewRecipeForm(forms.ModelForm):

    class Meta:
        model = Recipe
        fields = (
            'name',
            'description',
            'thumbnail',
            'predecessor',
            'ingredients',
            'steps',
            'difficulty',
            'StF_time', 
            'active_time',
            'attributes',
            'diet',
        )
