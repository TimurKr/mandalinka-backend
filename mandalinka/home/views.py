from django.views.generic import TemplateView

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

from django.contrib.auth import authenticate, login, logout

from home.forms import *
from home.models import Cities, Districts, PostalCodes, Streets

from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage

from .tokens import account_activation_token

class HomePageView(TemplateView):
    template_name = "home/home.html"

# Create your views here.

# Je toto vôbec niekedy použité??
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
            user = form.save(commit=False)
            user.is_active = False
            user.first_name = form.cleaned_data.get('firstname')
            user.last_name = form.cleaned_data.get('lastname')
            user.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            print(user.id)
            userProf = UserProfile.objects.get(user_name_id=user.id)
            email = form.cleaned_data.get('email')
            userProf.phone = form.cleaned_data.get("phone")
            userProf.street = form.cleaned_data.get("street")
            userProf.house_no =form.cleaned_data.get("house_no")
            userProf.city = form.cleaned_data.get("city")
            userProf.district = form.cleaned_data.get("district")
            userProf.postal = form.cleaned_data.get("postal")
            userProf.country = form.cleaned_data.get("country")
            userProf.food_preferences.set(form.cleaned_data.get("food_attr"))
            userProf.alergies.set(form.cleaned_data.get("alergies"))
            userProf.save()
            #send confirmation email
            mail_subject = 'Activate your user account.'
            message = render_to_string('home/template_activate_account.html', {
                'user': username,
                'domain': get_current_site(request).domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
                'protocol': 'https' if request.is_secure() else 'http'
            })
            mail = EmailMessage(mail_subject, message, to=[email])
            if mail.send():
                mess = f'Dear <b>{username}</b>, please go to you email <b>{email}</b> inbox and click on \
                    received activation link to confirm and complete the registration. <b>Note:</b> Check your spam folder.'
            else:
                mess= f'Problem sending confirmation email to {mail}, check if you typed it correctly.'
            return render(request, "home/home.html", {
                "message": mark_safe(mess),
                "message_type": "success",
            })
    else:
        form = SignupForm()
    districts = Districts.objects.all()
    cities = Cities.objects.all()
    postal_codes = PostalCodes.objects.all()
    streets = Streets.objects.all()
    return render(request, 'home/new_user.html',
                    {'form': form,
                     'districts': districts,
                     'cities': cities,
                     'postal_codes': postal_codes,
                     'streets': streets
    })

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, "home/login.html", {
                "message": 'Thank you for your email confirmation. Now you can login your account.',
                "message_type": "success",
                "form": LoginForm(),
            })
    else:
        return render(request, "home/login.html", {
                "message": 'Activation link is invalid!',
                "message_type": "danger",
                "form": LoginForm(),
            })

# def activateEmail(request, user, to_email):
#     mail_subject = 'Activate your user account.'
#     message = render_to_string('template_activate_account.html', {
#         'user': user.username,
#         'domain': get_current_site(request).domain,
#         'uid': urlsafe_base64_encode(force_bytes(user.pk)),
#         'token': account_activation_token.make_token(user),
#         'protocol': 'https' if request.is_secure() else 'http'
#     })
#     email = EmailMessage(mail_subject, message, to=[to_email])
#     if email.send():
#         messages.success(request, f'Dear <b>{user}</b>, please go to you email <b>{to_email}</b> inbox and click on \
#             received activation link to confirm and complete the registration. <b>Note:</b> Check your spam folder.')
#     else:
#         messages.error(request, f'Problem sending confirmation email to {to_email}, check if you typed it correctly.')