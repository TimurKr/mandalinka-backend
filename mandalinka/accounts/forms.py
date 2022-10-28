from django.contrib.auth import forms as auth_forms
from .models import User

from django.urls import reverse, reverse_lazy
from django.urls.exceptions import NoReverseMatch
from django.utils.translation import gettext_lazy as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, HTML, BaseInput, Field
from crispy_forms.bootstrap import StrictButton
from crispy_bootstrap5.bootstrap5 import FloatingField


class SubmitButton(BaseInput):
    input_type = 'submit'
    field_classes = 'btn btn-primary bg-gradient w-100 rounded-2 shadow'

class SecondaryButton(StrictButton):
    field_classes = 'btn btn-outline-primary w-100 rounded-2 shadow'

    def __init__(self, content, onclick: str = None, *args, **kwargs):
        if onclick:
            try:
                onclick = f'location.href="{reverse(onclick)}"'
            except NoReverseMatch:
                pass
            else:
                super().__init__(content, onclick=onclick, *args, **kwargs)
        super().__init__(content, *args, **kwargs)


class NewUserForm(auth_forms.UserCreationForm):
    class Meta:
        model = User
        fields = (
            "first_name",
            "pronoun",
            "last_name", 
            "email",
            "phone",
            "newsletter",
            "terms_conditions",
            "password1",
            "password2",
            )
        labels = {
            'newsletter': 'Súhlasíte so zasielaním propagačných emailov?',
            'terms_conditions': 'Súhlasíte s obchodnými podmienkami?',
        }
        help_texts = {
            'password1': None, 
            'password2': None,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['password1'].label = 'Heslo'
        self.fields['password2'].label = 'Heslo znova'
        self.fields['password1'].help_text = ''
        self.fields['password2'].help_text = ''
        self.fields['terms_conditions'].required = True
        
        self.helper = FormHelper(self)
        self.helper.form_action = reverse('accounts:new_user')
        self.helper.form_id = 'NewUserForm'
        self.helper.form_class = 'needs-validation'
        self.helper.attrs = {'novalidate': ''}
        self.helper.layout = Layout(
            Div(
                Div(FloatingField('first_name'), css_class='col-sm-4 col-6'),
                Div(FloatingField('pronoun'), css_class='col-sm-4 col-6'),
                Div(FloatingField('last_name'), css_class='col-sm-4'),
                Div(FloatingField('email'), css_class='col-sm-6'),
                Div(FloatingField('phone'), css_class='col-sm-6'),
                Div(FloatingField('password1'), css_class='col-12'),
                Div(FloatingField('password2'), css_class='col-12'),
                Div(Field('newsletter'), css_class='col-12 form-check form-switch ms-2 pe-2'),
                Div(Field('terms_conditions'), css_class='col-12 form-check form-switch ms-2 pe-2'),
                Div(SecondaryButton('Vrátiť domov'), css_class='col-sm-6'),
                Div(SubmitButton('submit', 'Vytvoriť účet'), css_class='col-sm-6'),
                css_class='row g-2'
            )
        )

    def save(self, commit=True):
        instance = super().save(commit=commit)
        instance.username = instance.first_name + '.' + instance.last_name + '.' + instance.email.split('@')[0]
        instance.save()
        return instance