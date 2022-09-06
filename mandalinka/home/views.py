from django.views.generic import TemplateView
<<<<<<< HEAD
from django.shortcuts import render
from recepty.models import Recipe

    # Create your views here.
def landing_page(request):
    return render(request, "home/landing_page.html", {
        "recipes": Recipe.objects.all(),
    })
=======
from django import forms
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

from django.contrib.auth import authenticate, login, logout

class HomePageView(TemplateView):
    template_name = "home/home.html"

class LoginForm(forms.Form):
    username = forms.CharField(label="username", widget=forms.TextInput({'class':'form-control'}))
    password = forms.CharField(label="password", widget=forms.PasswordInput())
 
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
                "message": "Invalid Credentials",
                "form": form
            })
    return render(request, "home/login.html", {
        "form": LoginForm()
    })

def logout_view(request):
    logout(request)
    return render(request, "home/login.html", {
                "message": "Logged Out",
                "form": LoginForm()
            })
>>>>>>> 5eed795bccf3da02612bfbee7b6f0110a8837eb6
