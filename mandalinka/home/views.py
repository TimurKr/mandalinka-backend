from django.views.generic import TemplateView

from django import forms
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

from django.contrib.auth import authenticate, login, logout

class HomePageView(TemplateView):
    template_name = "home/home.html"

class LoginForm(forms.Form):
    username = forms.CharField(label="username", widget=forms.TextInput({'class':'form-control rounded-5 opacity-25 shadow'}))
    password = forms.CharField(label="password", widget=forms.PasswordInput({'class':'form-control rounded-5 opacity-25 shodow'}))
 
# Create your views here.
def index(request):
    return render(request, "home/home.html")

def login_view(request):
    
    if request.method == "POST":
        print(request.POST)
        form = LoginForm(request.POST)
        # Accessing username and password from form data
        username = request.POST["username"]
        password = request.POST["password"]

        # Check if username and password are correct, returning User object if so
        user = authenticate(request, username=username, password=password)

        # If user object is returned, log in and route to index page:
        if user:
            login(request, user)
            return HttpResponseRedirect(reverse("home:home"))
        # Otherwise, return login page again with new context
        else:
            return render(request, "home/login.html", {
                "message": "Meno alebo heslo nesprávne",
                "message_type": "danger",
                "form": form
            })

    return render(request, "home/login.html", {
        "form": LoginForm()
    })

def logout_view(request):
    logout(request)
    return render(request, "home/home.html", {
                "message": "Boli ste úspešne odhlásený!",
                "message_type": "success",
                "form": LoginForm()
            })

def new_user_view(request):
    if request.method == "POST":
        print(request.POST)
    
    return render(request, "home/new_user.html")
