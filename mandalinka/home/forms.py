from email.policy import default
from ensurepip import bootstrap
from django import forms
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import forms as auth_forms
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _

from home.models import User, Address
from recepty.models import Alergen, FoodAttribute

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, HTML, Div, BaseInput, Submit, Field, Hidden
from crispy_forms.bootstrap import StrictButton
from crispy_bootstrap5.bootstrap5 import FloatingField
 

class CustomSubmitButton(BaseInput):
    input_type = 'submit'
    field_classes = 'btn btn-primary bg-gradient w-100 rounded-2 shadow'

class CustomSecondaryButton(StrictButton):
    field_classes = 'btn btn-outline-dark w-100 rounded-2 shadow'


# default_errors = {
#     'required': 'Toto pole je povinné',
#     'invalid': 'Zadajte valídnu hodnotu'
# }


class LoginForm(auth_forms.AuthenticationForm):

    error_messages = {
        "invalid_login": _("Zadajte valídny email a heslo."),
        "inactive": _("Tento účet je deaktivovaný. Kontaktujte nás."),
    }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_action = reverse('home:login')
        self.helper.form_id = 'LoginForm'
        self.helper.form_class = 'needs-validation'
        self.helper.attrs = {'novalidate':''}
        self.helper.layout = Layout(
                FloatingField('username', 'password'),
                HTML("<p> \
                    Zabudli ste heslo? Kliknite \
                    <a class='link-primary' href='{% url 'home:password_reset' %}'> \
                    sem</a>!</p>"
                ),
                Div(
                    Div(
                        CustomSecondaryButton('Zaregistrovať sa', 
                            onclick=f'location.href=\"{reverse("home:new_user")}\"'
                        ),
                        css_class='col-sm-6'
                    ),
                    Div(
                        CustomSubmitButton('submit', 'Prihlásiť sa'),
                        css_class='col-sm-6'
                    ),
                    css_class='row g-3'
                )
            )

    def get_user(self, request):
        return authenticate(
            request, 
            username=self.cleaned_data.get('username'), 
            password=self.cleaned_data.get('password')
            )


class NewUserForm(auth_forms.UserCreationForm):

    class Meta:
        model = User
        fields = ("first_name",
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
        self.helper.form_action = reverse('home:new_user')
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
                Div(StrictButton('Vrátiť domov', onclick=f'location.href=\"{reverse("home:home")}\"', css_class='secondary-button'), 
                    css_class='col-sm-6'),
                Div(Submit('submit', 'Vytvoriť účet',css_class="primary-button"), 
                    css_class='col-sm-6'),
                css_class='row g-2'
            )
        )

    def save(self, commit=True):
        instance = super().save(commit=commit)
        instance.username = instance.first_name + '.' + instance.last_name + '.' + instance.email.split('@')[0]
        instance.save()
        return instance
 
class PasswordResetForm(auth_forms.PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_action = reverse('home:password_reset')
        self.helper.form_id = 'PasswordResetForm'
        self.helper.form_class = 'needs-validation'
        self.helper.attrs = {'novalidate': ''}
        self.helper.layout = Layout(
            Div(
                Div(FloatingField('email'), css_class='col-sm-8'),
                Div(Submit('submit', 'Odoslať email', css_class="primary-button"), css_class="col-sm-4"),
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
        # self.helper.form_action = reverse('home:password_reset_set')
        self.helper.form_id = 'PasswordResetForm'
        self.helper.form_class = 'needs-validation'
        self.helper.attrs = {'novalidate': ''}
        self.helper.layout = Layout(
            Div(
                Div(FloatingField('new_password1'), css_class='col-sm-12'),
                Div(FloatingField('new_password2'), css_class='col-sm-12'),
                Div(Submit('submit', 'Nastaviť nové heslo', css_class="primary-button"), css_class="ms-sm-auto"),
                css_class='row g-2'
            )
        )

class BaseAddressForm(forms.ModelForm):

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
    def __init__(self,*args, **kwargs):
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
                StrictButton(self.secondary_button_title, onclick=f'location.href=\"{self.secondary_button_action}\"', css_class='secondary-button'), 
                    css_class='col-sm-6'),
        else: 
            secondary_button = None

        self.helper.layout = Layout(
            Div(
                Div(
                    HTML(
                        '<h5 class="title"> \
                            <span class="material-symbols-rounded">home_pin</span> \
                            Zadajte adresu doručenia \
                        </h5>'),
                    FloatingField('name'), 
                    FloatingField('address'),
                    FloatingField('note'),
                    FloatingField('city'),
                    FloatingField('district'),
                    FloatingField('postal'),
                    FloatingField('country'),
                    'coordinates',
                    css_class='map-panel col-sm-6 col-12'
                ),
                Div(css_class='map col-sm-6 col-12', css_id='gmp-map'),
                secondary_button,
                Div(Submit('submit', 'Uložiť', css_class="primary-button"), 
                    css_class='col-sm-6 ms-auto'),
                css_class='address-selection row g-3'
            ),
            HTML('<script src="https://maps.googleapis.com/maps/api/js?key=AIzaSyCEZTFyo0Kf5YL5SWe6vmmfEMmF5QxSTbU&libraries=places&callback=initMap&solution_channel=GMP_QB_addressselection_v1_cABC" async defer></script>'),
        )

class AddFirstAddress(BaseAddressForm):
    # form_action = reverse('home:home') ??????????????????????????
    form_id = 'first-address'

class AddAddressForm(BaseAddressForm):
    form_action = reverse_lazy('home:add_address')
    form_id = 'add-address'
    secondary_button_action = reverse_lazy('home:manage_addresses')
    secondary_button_title = 'Naspäť'

class EditAddressForm(BaseAddressForm):
    form_id = 'edit-address'
    secondary_button_action = reverse_lazy('home:manage_addresses')
    secondary_button_title = 'Naspäť'
    def __init__(self, address_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.form_action = reverse('home:edit_address', args=address_id)

class FoodPreferencesForm(forms.ModelForm):
    pass

# class SignupForm(UserCreationForm):

#         # Osobné veci
#     firstname = forms.CharField(
#         label="Meno", 
#         widget=forms.TextInput(charfield_widget),
#     )
#     lastname = forms.CharField(
#         label="Priezvisko",
#         widget=forms.TextInput(charfield_widget),
#     )
#     email = forms.EmailField(
#         label="Email", 
#         max_length=254, 
#         widget=forms.EmailInput(charfield_widget),
#     )
#     phone = forms.CharField(
#         label="Telefónne číslo",
#         help_text='Môže byť použité počas doručovania', 
#         required=True, 
#         min_length=5, 
#         widget=forms.TextInput(merge(charfield_widget,{'value':'+421'})),
#     )

#         # Newsletter a obchodné podmienky

#     newsletter = forms.BooleanField(
#         label="Súhlasíte so zasielaním propagačných emailov?", 
#         required=False,
#         widget=forms.CheckboxInput(checkbox_widget), 
#         )
#     terms_conditions = forms.BooleanField(
#         label="Súhlasíte so obchodnými podmienkami?",
#         required=True,
#         widget=forms.CheckboxInput(checkbox_widget),
#         )
    
#         # Preferencie 

#     num_portions = forms.ChoiceField(
#         label="Portions", 
#         help_text="Koľko porcí z každého jedla chcete dostávať?",
#         choices=UserProfile.portions_options,
#         initial=2,
#         widget=forms.RadioSelect(radioselect_widget), 
#     )
#     food_attributes = forms.ModelMultipleChoiceField(
#         label="Attributes", 
#         help_text="Zvolte obľúbené atribúty", 
#         queryset=FoodAttribute.objects.all(), 
#         required=False,
#         widget=forms.CheckboxSelectMultiple(radioselect_widget), 
#     )
#     alergies = forms.ModelMultipleChoiceField(
#         label="Alergens", 
#         help_text="Zvolte vaše alergie", 
#         queryset=Alergen.objects.all(), 
#         required=False,
#         widget=forms.CheckboxSelectMultiple(radioselect_widget), 
#     )
#     food_attributes.label_classes = radioselect_label_class
#     alergies.label_classes = radioselect_label_class

#         # Adresa

#     address = forms.CharField(
#         label="Ulica a číslo domu",
#         required=False,
#         widget=forms.TextInput(charfield_widget)
#     )

#     address_note = forms.CharField(
#         label="Poznámka pre kuriéra",
#         required=False,
#         widget=forms.TextInput(charfield_widget)
#     )
    
#     district = forms.CharField(
#         label="Mestská časť/Okres", 
#         required=False,
#         widget=forms.TextInput(charfield_widget)
#     )

#     city = forms.CharField(
#         label="Mesto", 
#         required=False, 
#         widget=forms.TextInput(charfield_widget)
#         )
#     postal = forms.CharField(
#         label="PSČ", 
#         required=False, 
#         widget=forms.TextInput(charfield_widget)
#     )

#     country = forms.CharField(
#         label="Krajina", 
#         required=False, 
#         widget=forms.TextInput(charfield_widget)
#     )

#     coordinates = forms.CharField(required=False, widget=forms.TextInput(attrs={'hidden':''}))

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['password1'].label = "Heslo"
#         self.fields['password1'].widget = forms.PasswordInput(attrs=charfield_widget)
#         self.fields['password2'].label = "Heslo znova"
#         self.fields['password2'].widget = forms.PasswordInput(attrs=charfield_widget)
#         self.fields['password2'].help_text = None


#     class Meta:
#         model = User
#         fields = ["firstname",
#                 "lastname", 
#                 "email",
#                 "phone",
#                 "newsletter",
#                 "terms_conditions",
#                 "num_portions",
#                 "food_attributes",
#                 "alergies",
#                 "address",
#                 "address_note",
#                 "city",
#                 "district",
#                 "postal",
#                 "country",
#                 "password1",
#                 "password2",
#                 "coordinates",
#                 ]

    # def clean_phone(self):
    #     data = self.cleaned_data['phone']
    #     if data[:4] not in ["+421", "+420"]:
    #         raise ValidationError("Unknown or missing dialing code")
    #     #if len(data) < 5:
    #      #   raise ValidationError("Phone number too short (must contain at least 5 numbers)")
    #     return data
    
    # def clean_house_no(self):
    #     data = self.cleaned_data['house_no']
    #     for i in data:
    #         if i not in '0123456789/-:':
    #             raise ValidationError("House number can only contain numbers or /-: characters")

    #     return data

    # def clean_district(self):
    #     data = self.cleaned_data['district']
    #     if not CityDistrictPostal.objects.filter(district=data).exists():
    #         raise ValidationError(f"Unknown district name {data}- make sure you choose from given list and use special characters")
    #     return data

    # def clean_city(self):
    #     data = self.cleaned_data['city']
    #     if not CityDistrictPostal.objects.filter(city=data).exists():
    #         raise ValidationError(f"Unknown city {data}- make sure you choose from given list and use special characters")
    #     return data

    # def clean_postal(self):
    #     data = self.cleaned_data['postal']
    #     #some streets have no postal codes in Bratislava (Adlerova, Alexyho...) - user should leave '-'
    #     if not CityDistrictPostal.objects.filter(postal=data).exists() and data != '-':
    #         raise ValidationError(f"Unknown postal code {data}- make sure you choose from given list and use special characters")
    #     return data

    # def clean_country(self):
    #     data = self.cleaned_data['country']
    #     if data not in ["SK", "CZ"]:
    #         raise ValidationError(f"Unknown country {data} - make sure you choose from given list and use special characters")
    #     return data

    # def clean(self):
    #     cleaned_data = super().clean()
    #     city = cleaned_data.get("city")
    #     district = cleaned_data.get("district")
    #     postal = cleaned_data.get("postal")
    #     address = cleaned_data.get("address")
    #     address_note = cleaned_data.get("address_note")
    #     valid_city = CityDistrictPostal.objects.filter(city=city, district=district)
    #     if not valid_city:
    #         # There is no such combination - the user probably used wrong district
    #         for_city = CityDistrictPostal.objects.filter(city=city)
    #         if not for_city:
    #             raise ValidationError(
    #                 mark_safe(f"We could not find city {city} in our database. Check the spelling, choose from suggested names or contact the admin")
    #             )
    #         # message = f'We only have following districts and postal codes (or streets) associated with city <strong>{city}</strong> and postal code <strong>{postal}</strong>: <ul>'
    #         # for obj in for_city:
    #         #     message += f'<li>District: <strong>{obj.district}</strong>, Postal code: <strong>{obj.postal}</strong>'
    #         #     if obj.street != '':
    #         #         message += f"Street: <strong>{obj.street}</strong>"
    #         #     message += '</li>'
    #         # message += "</ul>"
    #         self.add_error('city', mark_safe(f"Check if city {city} is in the district {district}"))
    #         self.add_error('district', mark_safe(f"Check if city {district} is in the given list"))
    #         raise ValidationError(
    #             mark_safe("Your address could not be found in our database. Please move somewhere else")
    #         )
    #     # then check if there is a city in that district with given postal code
    #     valid_city = CityDistrictPostal.objects.filter(city=city, district=district, postal=postal)
    #     num_res = valid_city.count()
    #     if num_res < 1 and postal != '-':
    #         # if there is no result
    #         exp = CityDistrictPostal.objects.filter(city=city)
    #         if not exp:
    #             raise ValidationError(mark_safe(f"No results for city <strong>{city}</strong>"))
    #         exp_distr = map(lambda x: x[0], exp.values_list("district").distinct())
    #         exp_post = [x[0] if x[0] != '' else '-' for x in exp.values_list("postal").distinct()]
    #         self.add_error('city', mark_safe(f"Check if city {city} is in the district {district} and has postal code {postal}"))
    #         self.add_error('district', mark_safe(f"Check if district {district} has the right postal code"))
    #         self.add_error('postal', mark_safe(f"Check if postal {postal} is associated with district {district}: if there is no postal code in your address fill in '-'"))
    #         raise ValidationError(
    #             mark_safe(f"""No results for provided address: {city}, {district}, {postal}.
    #             For city {city} there are only following districts to select:
    #             <strong><ul><li>{'</li><li>'.join(exp_distr)}</li></ul></strong>
    #             and only following postal codes:
    #             <strong><ul><li>{'</li><li>'.join(exp_post)}</li></ul></strong>""")
    #         )
    #     elif num_res == 1 and valid_city[0].street != '' and valid_city[0].street != street:
    #         #if there is only one row then it either needs additional info (street) or its enough
    #         if not street:
    #             self.add_error('street', mark_safe(f"For given address a street is required"))
    #         else:
    #             self.add_error('street', mark_safe(f"Check if street {street} is in the given list"))
    #         raise ValidationError(
    #             mark_safe(f"""We only have city <strong>{city}</strong>, district <strong>{district}</strong>, postal code <strong>{postal}</strong>
    #             associated with street <strong>{valid_city[0].street}</strong>. Check your input and try again.""")
    #         )
    #     elif num_res > 1:
    #         #If the query returns more than one then it has to depend on the street - checking that
    #         expected_streets = [x[0] for x in valid_city.values_list("street").distinct()]

    #         if street not in expected_streets:
    #             #if the provided street is not associated with any of the given city, district and postal than it has to be wrong
    #             self.add_error('street', mark_safe(f"Check given street"))
    #             self.add_error('postal', mark_safe(f"Check given postal {postal}: if there is no postal code in your address fill in '-'"))
    #             self.add_error('city', mark_safe(f"Check given city {city}"))

    #             raise ValidationError(
    #                     mark_safe(f"""We only have city <strong>{city}</strong>, district <strong>{district}</strong>, postal code <strong>{postal}</strong>
    #             associated with following streets:<strong><ul><li>{'</li><li>'.join(expected_streets)}</li></ul></strong>""")
    #             )

    #     valid_city = CityDistrictPostal.objects.filter(city=city, district=district, street=street)
    #     num_res = valid_city.count()
    #     if num_res < 1 and postal == '-':
    #         # if there is no result
    #         exp = CityDistrictPostal.objects.filter(city=city)
    #         if not exp:
    #             raise ValidationError(mark_safe(f"No results for city <strong>{city}</strong>"))
    #         exp_distr = map(lambda x: x[0], exp.values_list("district").distinct())
    #         exp_streets = [x[0] for x in exp.values_list("street").distinct()]
    #         self.add_error('city', mark_safe(f"Check if city {city} is in the district {district}"))
    #         self.add_error('district', mark_safe(f"Check if district {district} is in the options"))
    #         self.add_error('postal', mark_safe(f"Check if postal {postal} is associated with district {district}: if there is no postal code in your address fill in '-'"))
    #         raise ValidationError(
    #             mark_safe(f"""No results for provided address: {city}, {district}, {street} and no postal code.
    #             For city {city} there are only following districts to select:
    #             <strong><ul><li>{'</li><li>'.join(exp_distr)}</li></ul></strong>
    #             and only following streets with <strong>NO POSTAL CODE</strong>:
    #             <strong><ul><li>{'</li><li>'.join(exp_streets)}</li></ul></strong>""")
    #         )
    #     if num_res == 1 and valid_city[0].postal == '':
    #         # for some streets there are no postal codes provided - checking if that is the case
    #         if postal != '-':
    #             self.add_error('postal', mark_safe(f"If no postal is associated with your street fill in '-' or make sure postal code is from the list"))
    #             raise ValidationError(
    #                 mark_safe(f"For the city <strong>{city}</strong>, district <strong>{district}</strong> and street <strong>{street}</strong> there is no postal code and should be left '-'.")
    #             )
    #         if house_no == '':
    #             self.add_error('house_no', mark_safe(f"For this address house number is required"))

    #             raise ValidationError(
    #                 mark_safe(f"For the city <strong>{city}</strong>, district <strong>{district}</strong> and street <strong>{street}</strong> there is no postal code so a house number is required")
    #             )
    #     elif num_res > 1:
    #         # check if there is a postal code associated with the rest
    #         expected_postal = [x[0] if x[0] != '' else '-' for x in valid_city.values_list("postal").distinct()]
    #         if postal not in expected_postal:
    #             #if there is no valid combination with postal
    #             self.add_error('postal', mark_safe(f"Check if postal {postal} is associated with the district {district}: if there is no postal code in your address fill in '-'"))

    #             raise ValidationError(
    #                 mark_safe(f"""For the city <strong>{city}</strong>, district <strong>{district}</strong> and street <strong>{street}</strong>
    #                 there are only following postal codes provided: <strong><ul><li>{'</li><li>'.join(expected_postal)}</li></ul></strong>""")
    #             )

# class EditProfile(SignupForm):

#     def __init__(self,*args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.helper = FormHelper(self)
#         self.helper.form_action = reverse('home:my_account')
#         self.helper.form_id = 'LoginForm'
#         self.helper.form_class = 'needs-validation'
#         self.helper.attrs = {'novalidate':''}
#         self.fields.pop('password1')
#         self.fields.pop('password2')
