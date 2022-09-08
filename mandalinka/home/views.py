from django.views.generic import TemplateView

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

from django.contrib.auth import authenticate, login, logout

from home.forms import *

class HomePageView(TemplateView):
    template_name = "home/home.html"


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
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return render(request, "home/home.html", {
                "message": f"{username}, Vaše konto bolo úspešne zaregistrované",
                "message_type": "success",
            })
    else:
        form = SignupForm()
    return render(request, 'home/new_user.html', {'form': form})