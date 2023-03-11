from django.contrib.auth import forms as auth_forms
from django import forms

from .models import User, Address

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

    def __init__(self, content, onclick=None, *args, **kwargs):
        if onclick:
            onclick = f'location.href="{reverse(onclick)}"'
            super().__init__(content, onclick=onclick, *args, **kwargs)
        else:
            super().__init__(content, *args, **kwargs)

# BASICS ########################################################################


class LoginForm(auth_forms.AuthenticationForm):

    error_messages = {
        "invalid_login": _("Zadajte valídny email a heslo."),
        "inactive": _("Tento účet je deaktivovaný. Kontaktujte nás."),
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_action = reverse('accounts:login')
        self.helper.form_id = 'LoginForm'
        self.helper.form_class = 'needs-validation'
        self.helper.attrs = {'novalidate': ''}
        self.helper.layout = Layout(
            FloatingField('username', 'password'),
            HTML("<p> \
                    Zabudli ste heslo? Kliknite \
                    <a class='link-primary' href='{% url 'accounts:password_reset' %}'> \
                    sem</a>!</p>"
                 ),
            Div(
                Div(
                    SecondaryButton('Zaregistrovať sa',
                                    onclick='accounts:new_user'),
                    css_class='col-sm-6'
                ),
                Div(
                    SubmitButton('submit', 'Prihlásiť sa'),
                    css_class='col-sm-6'
                ),
                css_class='row g-3'
            )
        )

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

        self.helper = FormHelper(self)
        self.helper.form_action = reverse('accounts:new_user')
        self.helper.form_id = 'NewUserForm'
        self.helper.form_class = 'needs-validation'
        self.helper.attrs = {'novalidate': ''}
        self.helper.layout = Layout(
            Div(
                Div(FloatingField('first_name', autofocus=True),
                    css_class='col-sm-4 col-6'),
                Div(FloatingField('pronoun'), css_class='col-sm-4 col-6'),
                Div(FloatingField('last_name'), css_class='col-sm-4'),
                Div(FloatingField('email'), css_class='col-12'),
                Div(FloatingField('phone'), css_class='col-12'),
                Div(FloatingField('password1'), css_class='col-12'),
                Div(FloatingField('password2'), css_class='col-12'),
                Div(Field('newsletter'),
                    css_class='col-12 form-check form-switch ms-2 pe-2'),
                Div(Field('terms_conditions'),
                    css_class='col-12 form-check form-switch ms-2 pe-2'),
                Div(SecondaryButton('Naspäť', onclick='customers:home_page'),
                    css_class='col-sm-6'),
                Div(SubmitButton('submit', 'Vytvoriť účet'), css_class='col-sm-6'),
                css_class='row g-2'
            )
        )

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

        self.helper = FormHelper(self)
        self.helper.form_action = reverse_lazy('accounts:edit_general')
        self.helper.form_id = 'general_info'
        self.helper.form_class = 'needs-validation'
        self.helper.attrs = {'novalidate': ''}
        self.helper.layout = Layout(
            Div(
                Div(FloatingField('first_name'), css_class='col-8'),
                Div(FloatingField('pronoun'), css_class='col-4'),
                Div(FloatingField('last_name'), css_class='col-12'),
                Div(FloatingField('phone'), css_class='col-12'),
                Div(Field('newsletter'),
                    css_class='col-12 form-check form-switch ms-2 pe-2'),
                Div(Field('terms_conditions'),
                    css_class='col-12 form-check form-switch ms-2 pe-2'),
                Div(SecondaryButton(
                    'Zmeniť heslo', onclick="accounts:password_change"), css_class='col-sm-4 col-6'),
                Div(SecondaryButton(
                    'Zmeniť email', onclick="accounts:email_change"), css_class='col-sm-4 col-6'),
                Div(SubmitButton('submit', 'Uložiť'),
                    css_class='col-sm-4'),
                Div(SecondaryButton('Deaktivovať účet', onclick="accounts:deactivate",
                    css_class='danger-button'), css_class='col-auto ms-auto'),
                css_class='row g-2'
            )
        )

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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['coordinates'].widget = forms.HiddenInput()

        self.helper = FormHelper(self)

        try:
            self.helper.form_id = self.form_id
        except:
            self.helper.form_id = None
        try:
            self.helper.form_action = self.form_action
        except:
            self.helper.form_action = None

        self.helper.form_class = 'needs-validation'
        self.helper.attrs = {'novalidate': ''}

        if self.secondary_button_action and self.secondary_button_title:
            secondary_button = Div(
                SecondaryButton(self.secondary_button_title,
                                onclick=self.secondary_button_action),
                css_class='col-sm-6')
        else:
            secondary_button = None

        self.helper.layout = Layout(
            Div(
                Div(
                    FloatingField('name'),
                    FloatingField('address'),
                    FloatingField('note'),
                    FloatingField('city'),
                    FloatingField('district'),
                    FloatingField('postal'),
                    FloatingField('country'),
                    'coordinates',
                    css_class='map-panel col-md-6 col-12'
                ),
                Div(css_class='map col-md-6 col-12', css_id='gmp-map'),
                secondary_button,
                Div(SubmitButton('submit', 'Uložiť'),
                    css_class='col-sm-6 ms-auto'),
                css_class='address-selection row g-3'
            ),
            HTML('<script src="https://maps.googleapis.com/maps/api/js?key=AIzaSyCEZTFyo0Kf5YL5SWe6vmmfEMmF5QxSTbU&libraries=places&callback=initMap&solution_channel=GMP_QB_addressselection_v1_cABC" async defer></script>'),
        )

    def save(self, commit=True):
        try:
            return super().save(commit=commit)
        except ValueError:
            if self.errors.get('coordinates', None):
                self.add_error('address', ValidationError(
                    'Pri zadávaní adresy zvolte z ponúkaného výberu. Uistite sa, že sa na mape zobrazuje správna adresa.', 'no_coordinates'))
            return super().save(commit=commit)


class FirstAddressForm(BaseAddressForm):
    form_action = reverse_lazy('accounts:add_first_address')
    form_id = 'first-address'


class AddAddressForm(BaseAddressForm):
    form_action = reverse_lazy('accounts:add_address')
    form_id = 'add-address'
    secondary_button_action = 'accounts:my_account'
    secondary_button_title = 'Naspäť'


class EditAddressForm(BaseAddressForm):
    form_id = 'edit-address'
    secondary_button_action = 'accounts:my_account'
    secondary_button_title = 'Naspäť'

    def __init__(self, address_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.form_action = reverse(
            'accounts:edit_address', args=(address_id,))

# PREFERENCES ##################################################################


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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_action = reverse('accounts:edit_preferences')
        self.helper.form_id = 'edit-preferences'
        self.helper.form_class = 'needs-validation'
        self.helper.attrs = {'novalidate': ''}
        self.helper.layout = Layout(
            'default_num_portions',
            'food_preferences',
            'diet',
            'alergies',
            Div(Field('default_pickup'), css_class='form-check form-switch'),
            Div(Div(SubmitButton('submit', 'Uložiť'),
                css_class='col-6 ms-auto mt-3'), css_class='row')
        )


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

        self.helper = FormHelper(self)
        self.helper.form_id = 'PasswordChangeForm'
        self.helper.form_class = 'needs-validation'
        self.helper.attrs = {'novalidate': ''}
        self.helper.layout = Layout(
            Div(
                Div(FloatingField('old_password'), css_class='col-12, pb-3'),
                Div(FloatingField('new_password1'), css_class='col-12'),
                Div(FloatingField('new_password2'), css_class='col-12'),
                Div(SecondaryButton('Naspäť', 'accounts:my_account'),
                    css_class="col-auto ms-sm-auto"),
                Div(SubmitButton('submit', 'Nastaviť nové heslo'),
                    css_class="col-auto"),
                css_class='row g-2'
            )
        )


class PasswordResetForm(auth_forms.PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_action = reverse('accounts:password_reset')
        self.helper.form_id = 'PasswordResetForm'
        self.helper.form_class = 'needs-validation'
        self.helper.attrs = {'novalidate': ''}
        self.helper.layout = Layout(
            Div(
                Div(FloatingField('email'), css_class='col-12'),
                Div(SecondaryButton('Naspäť', 'accounts:login'),
                    css_class="col-auto ms-auto"),
                Div(SubmitButton('submit', 'Odoslať'), css_class="col-auto"),
                css_class='row g-2'
            )
        )


class SetPasswordForm(auth_forms.SetPasswordForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(user, *args, **kwargs)

        self.fields['new_password1'].label = 'Heslo'
        self.fields['new_password2'].label = 'Heslo znova'
        self.fields['new_password1'].help_text = ''
        self.fields['new_password2'].help_text = ''

        self.helper = FormHelper(self)
        self.helper.form_id = 'PasswordResetForm'
        self.helper.form_class = 'needs-validation'
        self.helper.attrs = {'novalidate': ''}
        self.helper.layout = Layout(
            Div(
                Div(FloatingField('new_password1'), css_class='col-12'),
                Div(FloatingField('new_password2'), css_class='col-12'),
                Div(SubmitButton('submit', 'Nastaviť nové heslo'),
                    css_class="col-auto ms-auto"),
                css_class='row g-2'
            )
        )