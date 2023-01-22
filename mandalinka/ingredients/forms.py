from django import forms
from django.urls import reverse_lazy

from .models import Ingredient, IngredientVersion

from utils.forms import SubmitButton, SecondarySubmitButton
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

# class EditIngredientForm(NewIngredientForm):
#     def __init__(self, ingredient_id, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.helper.form_action = reverse_lazy('recipes:edit_ingredient', args=(ingredient_id, ))