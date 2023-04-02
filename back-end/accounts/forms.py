from django.contrib.auth import forms as auth_forms
from django import forms

from .models import User, Address

from django.core.exceptions import ValidationError

from django.urls import reverse, reverse_lazy
from django.urls.exceptions import NoReverseMatch
from django.utils.translation import gettext_lazy as _

# BASICS ########################################################################


class LoginForm(auth_forms.AuthenticationForm):

    error_messages = {
        "invalid_login": _("Zadajte valídny email a heslo."),
        "inactive": _("Tento účet je deaktivovaný. Kontaktujte nás."),
    }

# GENERAL ######################################################################


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
            'newsletter': 'Súhlasíte so zasielaním reklamných emailov?',
            'terms_conditions': 'Súhlasíte s obchodnými podmienkami?',
        }
        help_texts = {
            'password1': None,
            'password2': None,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['password1'].label = 'Heslo'
        self.fields['password2'].label = 'Potvrďte heslo'
        self.fields['password1'].help_text = ''
        self.fields['password2'].help_text = ''
        self.fields['terms_conditions'].required = True

    def save(self, commit=True):
        instance = super().save(commit=commit)
        instance.username = instance.first_name + '.' + \
            instance.last_name + '.' + instance.email.split('@')[0]
        instance.save()
        return instance


class GeneralUserInfoForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            "first_name",
            "pronoun",
            "last_name",
            "phone",
            "newsletter",
            "terms_conditions",
        )
        labels = NewUserForm.Meta.labels

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['terms_conditions'].required = True

# ADDRESS #######################################################################


class BaseAddressForm(forms.ModelForm):
    secondary_button_action = None
    secondary_button_title = None

    class Meta:
        model = Address
        fields = (
            'name',
            'address',
            'note',
            'city',
            'district',
            'postal',
            'country',
            'coordinates',
        )

    def save(self, commit=True):
        try:
            return super().save(commit=commit)
        except ValueError:
            if self.errors.get('coordinates', None):
                self.add_error('address', ValidationError(
                    'Pri zadávaní adresy zvolte z ponúkaného výberu. Uistite sa, že sa na mape zobrazuje správna adresa.', 'no_coordinates'))
            return super().save(commit=commit)


class PreferencesForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            'default_num_portions',
            'default_pickup',
            'food_preferences',
            'alergies',
            'diet',
        )
        widgets = {
            'food_preferences': forms.CheckboxSelectMultiple(),
            'alergies': forms.CheckboxSelectMultiple(),
            'default_num_portions': forms.RadioSelect(),
            'diet': forms.CheckboxSelectMultiple(),
        }


class SetPreferencesForm(PreferencesForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.form_action = reverse('accounts:set_preferences')

# PASSWORD MANIPULATION ###############################################################


class PasswordChangeForm(auth_forms.PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['old_password'].label = 'Staré heslo'
        self.fields['new_password1'].label = 'Heslo'
        self.fields['new_password2'].label = 'Heslo znova'
        self.fields['old_password'].help_text = ''
        self.fields['new_password1'].help_text = ''
        self.fields['new_password2'].help_text = ''


class PasswordResetForm(auth_forms.PasswordResetForm):
    pass


class SetPasswordForm(auth_forms.SetPasswordForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(user, *args, **kwargs)

        self.fields['new_password1'].label = 'Heslo'
        self.fields['new_password2'].label = 'Heslo znova'
        self.fields['new_password1'].help_text = ''
        self.fields['new_password2'].help_text = ''
