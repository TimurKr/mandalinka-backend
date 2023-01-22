from django import forms

from .models import Recipe, IngredientInRecipe, IngredientVersion, Step

from django.core.exceptions import ValidationError, NON_FIELD_ERRORS

from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _

from django.contrib.admin.forms import *

from utils.forms import SubmitButton
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div


# RECIPES #######################################################################

class RecipeForm(forms.ModelForm):

    class Meta:
        model = Recipe
        fields = (
            'predecessor',
            'exclusive_inheritance',
            'name',
            'description',
            'description_finished',
            'thumbnail',
            'difficulty',
            'cooking_time', 
            'active_cooking_time',
            'attributes',
            'diet',
            'required_accessories',
            'todo',
            'created_by',
        )
        widgets = {
            'diet': forms.CheckboxSelectMultiple(),
            'attributes': forms.CheckboxSelectMultiple(),
            'required_accessories': forms.CheckboxSelectMultiple(),
            'todo': forms.Textarea(attrs={'rows': '3'}),
            'description': forms.Textarea(attrs={'rows': '3'}),
            'steps': forms.Textarea(attrs={'rows': '5'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_id = 'general_info'
        self.helper.form_class = 'needs-validation'
        self.helper.attrs = {'novalidate': ''}

    def clean(self):
        cleaned_data = super().clean()

        if cleaned_data.get("cooking_time") < cleaned_data.get("active_cooking_time"):
            self.add_error('cooking_time', "Čas varenia musí byť väčší alebo rovný aktívnemu času varenia")
            self.add_error('active_cooking_time', "Čas varenia musí byť väčší alebo rovný aktívnemu času varenia")


class NewRecipeForm(RecipeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.form_action = reverse_lazy('recipes:add')
        self.helper.layout = Layout(
            'predecessor',
            'exclusive_inheritance',
            'name',
            'description',
            'description_finished',
            'thumbnail',
            'difficulty',
            'cooking_time', 
            'active_cooking_time',
            'attributes',
            'diet',
            'required_accessories',
            'todo',
            'created_by',
            SubmitButton('Submit', 'Vytvoriť nový recept'),
        )

    class Media:
        js = ("recipes/js/add.js",)

class EditRecipeForm(RecipeForm):
    def __init__(self, recipe_id, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['created_by'].disabled = True

        self.helper.form_tag = False
        self.helper.layout = Layout(
            'name',
            'predecessor',
            'exclusive_inheritance',
            'description',
            'description_finished',
            'thumbnail',
            'difficulty',
            'cooking_time', 
            'active_cooking_time',
            'attributes',
            'diet',
            'required_accessories',
            'todo',
            Div(
                Div(SubmitButton('submit', 'Uložiť všeobecné informácie'), css_class='col-auto ms-auto'),
                css_class='row g-2'
            )
        )

    class Media:
        js = ("recipes/js/edit_recipe.js",)


class IngredientInRecipeForm(forms.ModelForm):
    class Meta:
        model = IngredientInRecipe
        fields = ('ingredient', 'amount')
        widgets = {
            'ingredient': forms.Select(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        queryset = IngredientVersion.objects.filter(status=IngredientVersion.Statuses.ACTIVE)
        if self.instance.pk:
            queryset = queryset | IngredientVersion.objects.filter(pk=self.instance.ingredient.pk)
        self.fields['ingredient'].queryset = queryset
    
IngredientInRecipeFormset = forms.inlineformset_factory(Recipe, IngredientInRecipe, 
    form=IngredientInRecipeForm, 
    extra=2,
    max_num=16,
    validate_max=True,
    )


class StepForm(forms.ModelForm):
    class Meta:
        model = Step
        fields = ('number', 'text', 'thumbnail')
        widgets = {
            'text': forms.Textarea(attrs={'rows': 2}),
        }
        error_messages = {
            NON_FIELD_ERRORS: {
                'unique_together': "%(field_labels)s: Krok pre daný recept s týmto číslom už existuje.",
            }
        }

StepFormset = forms.modelformset_factory(Step, 
    form=StepForm,
    extra=2,
    max_num=8,
    validate_max=True,
    )

    
        

# INGREDIENTS #######################################################################

