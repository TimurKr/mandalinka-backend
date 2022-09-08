from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from address.forms import AddressField
from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(label="username", widget=forms.TextInput({'class':'form-control rounded-5 opacity-25 shadow'}))
    password = forms.CharField(label="password", widget=forms.PasswordInput({'class':'form-control rounded-5 opacity-25 shodow'}))
 
 
class SignupForm(UserCreationForm):
    COUNTRIES = (
        ("1","SK"),
        ("2","CZ"),
        ("3", "ine")
    )
    email = forms.EmailField(label="Email", max_length=254, help_text='Emailová adresa')
    phone = forms.CharField(label="Ulica",help_text='Tel.číslo:')

    street = forms.CharField(label="street",help_text='Ulica:')
    house_no = forms.CharField(label="house_no",help_text='Číslo domu:')
    city = forms.CharField(label="city",help_text='Mesto:')
    postal = forms.CharField(label="postal",help_text='PSČ:')
    country = forms.ChoiceField(label="country",choices=COUNTRIES, help_text='Krajina:')
    
    class Meta:
        model = User
        fields = ["username", "email","phone", "street", "house_no", "city", "postal", "country","password1", "password2"]