from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(label="username", widget=forms.TextInput({'class':'form-control'}))
    password = forms.CharField(label="password", widget=forms.PasswordInput())
 
class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]