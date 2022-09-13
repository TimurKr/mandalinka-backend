from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe
from home.models import CityDistrictPostal, Districts, Cities, PostalCodes, UserProfile, FoodAttribute
from recepty.models import Alergen

charfield_widget = {'class': 'form-control opacity-75 rounded-2 shadow border-dark',
                    'placeholder': 'Password'}
checkbox_widget = {'class':'form-check-input'}
select_widget = {'class':'form-select form-select opacity-75 rounded-2 shadow border-dark'}

def merge(dict1, dict2):
    return {**dict1, **dict2} 

class LoginForm(forms.Form):
    username = forms.CharField(label="Prihlasovacie meno", widget=forms.TextInput(charfield_widget))
    password = forms.CharField(label="Heslo", widget=forms.PasswordInput(charfield_widget))
 
 
class SignupForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = "Prihlasovacie meno"
        self.fields['username'].help_text = 'Username (150 characters or fewer, letters, digits and @/./+/-/_ only)'
        self.fields['username'].widget = forms.TextInput(charfield_widget)
        self.fields['password1'].widget = forms.PasswordInput(attrs=charfield_widget)
        self.fields['password2'].widget = forms.PasswordInput(attrs=charfield_widget)


    COUNTRIES = (
        ("CZ","SK"),
        ("SK","CZ"),
    )
    firstname = forms.CharField(label="Meno", widget=forms.TextInput(charfield_widget))
    lastname = forms.CharField(label="Priezvisko", widget=forms.TextInput(charfield_widget))
    email = forms.EmailField(label="Email", max_length=254, widget=forms.EmailInput(charfield_widget))
    phone = forms.CharField(min_length=5, label="Telefónne číslo", help_text='Môže byť použité počas doručovania', required=True, widget=forms.TextInput(merge(charfield_widget,{'value':'+421'})))

    newsletter = forms.BooleanField(label="Súhlasíte so zasielaním propagačných emailov?",
                                    help_text="Súhlasíte so zasielaním propagačných emailov?", 
                                    widget=forms.CheckboxInput(checkbox_widget))
    terms_conditions = forms.BooleanField(label="Súhlasíte so obchodnými podmienkami?",
                                            widget=forms.CheckboxInput(checkbox_widget),
                                            required=True)
    
    num_portions = forms.ChoiceField(label="Portions", help_text="Koľko porcí z každého jedla chcete dostávať?",
                                        choices=UserProfile.portions_options,
                                        widget=forms.RadioSelect())
    food_attributes = forms.ModelMultipleChoiceField(label="Attributes", help_text="Zvolte obľúbené atribúty", 
                                                queryset=FoodAttribute.objects.all(), 
                                                widget=forms.CheckboxSelectMultiple())
    alergies = forms.ModelMultipleChoiceField(label="Alergens", help_text="Zvolte vaše alergie", 
                                                queryset=Alergen.objects.all(), 
                                                widget=forms.CheckboxSelectMultiple())

    street = forms.CharField(label="Ulica",required=False, widget=forms.TextInput(merge(charfield_widget,{'list':'streets'})))
    house_no = forms.CharField(label="Číslo domu", required=True, widget=forms.TextInput(charfield_widget))
    district = forms.CharField(label="Mestská časť",required=True, widget=forms.TextInput(merge(charfield_widget, {'list':'districts'})))
    city = forms.CharField(label="Mesto",required=True, widget=forms.TextInput(merge(charfield_widget,{'list':'cities'})))
    postal = forms.CharField(min_length=5, max_length=5,label="PSČ",required=True, widget=forms.TextInput(merge(charfield_widget,{'list':'postal_codes'})))
    country = forms.ChoiceField(label="Krajina",choices=COUNTRIES, required=True, widget=forms.Select(select_widget))
    
    class Meta:
        model = User
        fields = ["username",
                "firstname",
                "lastname", 
                "email",
                "phone",
                "newsletter",
                "terms_conditions",
                "num_portions",
                "food_attributes",
                "alergies",
                "street",
                "house_no",
                "city",
                "district",
                "postal",
                "country",
                "password1",
                "password2"
                ]

    def clean_phone(self):
        data = self.cleaned_data['phone']
        if data[:4] not in ["+421", "+420"]:
            raise ValidationError("Unknown or missing dialing code")
        #if len(data) < 5:
         #   raise ValidationError("Phone number too short (must contain at least 5 numbers)")

        return data
    
    def clean_house_no(self):
        data = self.cleaned_data['house_no']
        for i in data:
            if i not in '0123456789/-:':
                raise ValidationError("House number can only contain numbers or /-: characters")

        return data

    def clean_district(self):
        data = self.cleaned_data['district']
        if not Districts.objects.filter(district=data).exists():
            raise ValidationError("Unknown district name - make sure you choose from given list and use special characters")
        return data

    def clean_city(self):
        data = self.cleaned_data['city']
        if not Cities.objects.filter(city=data).exists():
            raise ValidationError("Unknown city - make sure you choose from given list and use special characters")
        return data

    def clean_postal(self):
        data = self.cleaned_data['postal']
        if not PostalCodes.objects.filter(code=data).exists():
            raise ValidationError("Unknown postal code - make sure you choose from given list and use special characters")
        return data

    def clean_country(self):
        data = self.cleaned_data['country']
        if data not in ["SK", "CZ"]:
            raise ValidationError("Unknown country - make sure you choose from given list and use special characters")
        return data

    def clean(self):
        cleaned_data = super().clean()
        city = cleaned_data.get("city")
        district = cleaned_data.get("district")
        postal = cleaned_data.get("postal")
        valid_city = CityDistrictPostal.objects.filter(city=city, district=district, postal=postal)
        if not valid_city:
            # There is no such combination - the user probably user wrong postal code or district
            
            for_city = CityDistrictPostal.objects.filter(city=city)
            if not for_city:
                raise ValidationError(
                    f"We could not find city {city} in out database. Check the spelling, choose from suggested names or contact the admin"
                )
            message = f'We only have following districts and postal codes associated with city <strong>{city}</strong>: <ul>'
            for obj in for_city:
                message += f'<li>District: <strong>{obj.district}</strong>, Postal code: <strong>{obj.postal}</strong></li>'
            message += "</ul>"
            raise ValidationError(
                mark_safe(message)
            )