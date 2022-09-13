from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from home.models import CityDistrictPostal, Districts, Cities, PostalCodes
from django import forms
from django.core.exceptions import ValidationError
from home.models import UserProfile, Food_attr
from django.utils.safestring import mark_safe

charfield_widget = {'class': 'form-control opacity-75 rounded-2 shadow border-dark',
                    'placeholder': 'useless_placeholder'}
checkbox_widget = {'class':'form-check-input'}

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

    COUNTRIES = (
        ("CZ","SK"),
        ("SK","CZ"),
    )
    firstname = forms.CharField(label="Meno", widget=forms.TextInput(charfield_widget))
    lastname = forms.CharField(label="Priezvisko", widget=forms.TextInput(charfield_widget))
    email = forms.EmailField(label="Email", max_length=254, widget=forms.EmailInput(charfield_widget))

    newsletter = forms.BooleanField(label="Súhlasíte so zasielaním propagačných emailov?",
                                    help_text="Súhlasíte so zasielaním propagačných emailov?", 
                                    widget=forms.CheckboxInput(checkbox_widget))
    terms_conditions = forms.BooleanField(help_text="Súhlasíte s <a hrf='#Obchodné podmienky'>obchodnými podmienkami</a>?",
                                          required=True)
    
    food_attr = forms.ModelMultipleChoiceField(label="Attributes", help_text="Zvolte obľúbené atribúty", queryset=Food_attr.objects.all(), widget=forms.CheckboxSelectMultiple)

    phone = forms.CharField(min_length=5, label="Telefónne číslo", help_text='* Môže byť použité počas doručovania', required=True, widget=forms.TextInput(merge(charfield_widget,{'value':'+421'})))

    street = forms.CharField(label="street",help_text='Ulica:',required=False, widget=forms.TextInput(attrs={'list':'streets'}))
    house_no = forms.CharField(label="house_no",help_text='Číslo domu:', required=True)
    district = forms.CharField(label="district",help_text='Okres:',required=True, widget=forms.TextInput(attrs={'list':'districts'}))
    city = forms.CharField(label="city",help_text='Mesto:',required=True, widget=forms.TextInput(attrs={'list':'cities'}))
    postal = forms.CharField(min_length=5, max_length=5,label="postal", help_text='PSČ:',required=True, widget=forms.TextInput(attrs={'list':'postal_codes'}))
    country = forms.ChoiceField(label="country",choices=COUNTRIES, required=True, help_text='Krajina:')
    
    class Meta:
        model = User
        fields = ["username",
                "firstname",
                "lastname", 
                "email",
                "newsletter",
                "terms_conditions",
                "food_attr",
                "phone",
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