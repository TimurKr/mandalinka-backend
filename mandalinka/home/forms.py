from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from home.models import Districts, Cities, PostalCodes
from django import forms
from django.core.exceptions import ValidationError
from home.models import UserProfile

class LoginForm(forms.Form):
    username = forms.CharField(label="username", widget=forms.TextInput({'class':'form-control rounded-5 opacity-25 shadow'}))
    password = forms.CharField(label="password", widget=forms.PasswordInput({'class':'form-control rounded-5 opacity-25 shodow'}))
 
 
class SignupForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = 'Username (150 characters or fewer, letters, digits and @/./+/-/_ only) '

    COUNTRIES = (
        ("CZ","SK"),
        ("SK","CZ"),
    )
    email = forms.EmailField(label="Email", max_length=254, help_text='Emailová adresa')
    phone = forms.CharField(label="Ulica",help_text='Tel.číslo:',required=True, widget=forms.TextInput(attrs={'value':'+421'}))

    street = forms.CharField(label="street",help_text='Ulica:',required=False, widget=forms.TextInput(attrs={'list':'streets'}))
    house_no = forms.CharField(label="house_no",help_text='Číslo domu:', required=True)
    district = forms.CharField(label="district",help_text='Okres:',required=True, widget=forms.TextInput(attrs={'list':'districts'}))
    city = forms.CharField(label="city",help_text='Mesto:',required=True, widget=forms.TextInput(attrs={'list':'cities'}))
    postal = forms.CharField(label="postal", help_text='PSČ:',required=True, widget=forms.TextInput(attrs={'list':'postal_codes'}))
    country = forms.ChoiceField(label="country",choices=COUNTRIES, required=True, help_text='Krajina:')
    
    class Meta:
        model = User
        fields = ["username", 
                "email",
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
        if len(data) < 5:
            raise ValidationError("Phone number too short (must contain at least 5 numbers)")

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