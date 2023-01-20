from django import forms

from .models import Recipe, IngredientInRecipe, IngredientVersion, Step

from django.core.exceptions import ValidationError, NON_FIELD_ERRORS

from django.urls import reverse, reverse_lazy
from django.urls.exceptions import NoReverseMatch
from django.utils.translation import gettext_lazy as _

from django.contrib.admin.forms import *

from django.db.models import Case, When

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

    class Meta:
        model = Recipe
        fields = (
            'predecessor',
            'exclusive_predecessor',
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
        self.helper.form_action = reverse_lazy('recipes:add_recipe')
        self.helper.layout = Layout(
            'predecessor',
            'exclusive_predecessor',
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
        js = ("recipes/js/add_recipe.js",)

class EditRecipeForm(RecipeForm):
    def __init__(self, recipe_id, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['created_by'].disabled = True

        self.helper.form_tag = False
        self.helper.layout = Layout(
            'name',
            'predecessor',
            'exclusive_predecessor',
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

# class IngredientForm(forms.ModelForm):

#     class Meta:
#         model = Ingredient
#         fields = (
#             'name', 
#             'img', 
#             'unit',
#             'price_per_unit',
#             'alergens',
#         )
#         widgets = {
#             'alergens': forms.CheckboxSelectMultiple(),
#         }

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.helper = FormHelper(self)
#         self.helper.form_class = 'needs-validation'
#         self.helper.attrs = {'novalidate': ''}
#         self.helper.layout = Layout(
#             'name', 
#             'img', 
#             'unit',
#             'price_per_unit',
#             'alergens',
#             Div(
#                 Div(SecondarySubmitButton('submit', 'Uložiť a vrátiť'), css_class='col-sm-6'),
#                 Div(SubmitButton('submit', 'Uložiť a upravi'), css_class='col-sm-6'),
#                 css_class='row g-2'
#             )
#         )

# class NewIngredientForm(IngredientForm):
#     def __init__(self,*args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.helper.form_action = reverse_lazy('recipes:add_ingredient')

# class EditIngredientForm(NewIngredientForm):
#     def __init__(self, ingredient_id, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.helper.form_action = reverse_lazy('recipes:edit_ingredient', args=(ingredient_id, ))