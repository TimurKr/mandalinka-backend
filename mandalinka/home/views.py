from time import sleep
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseBadRequest, JsonResponse
from django.urls import reverse
from django.db.models.query_utils import Q
from django.template.loader import render_to_string
from django.core.mail import send_mail, EmailMessage, BadHeaderError

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site


from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str

from home.forms import *
from home.models import Streets, Order
from recepty.models import RecipeOrderInstance
import json
from .tokens import account_activation_token



# Create your views here.
def index(request):
    context = {
        "loginform": LoginForm(),
    }
    return render(request, "home/home.html", context)


def login_view(request):
    if request.method == "POST":
        print(request)
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
            form = LoginForm(request.POST)
            form.add_error(None, "Email alebo heslo nesprávne")
            context = {
                "loginform": form,
                "focus": "LoginModal",
            }
            return render(request, "home/home.html", context)
    return HttpResponseRedirect(reverse("home:home"))



def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("home:home"))


def new_user_view(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.first_name = form.cleaned_data.get("firstname")
            user.last_name = form.cleaned_data.get("lastname")
            user.email = form.cleaned_data.get("email")
            user.username = user.first_name + user.last_name + user.email.split('@')[0]
            user.save()     
            userProf = UserProfile.objects.get(user_name_id = user.id)     
            userProf.phone = form.cleaned_data.get("phone")
            userProf.newsletter = form.cleaned_data.get("newsletter")
            userProf.terms_conditions = form.cleaned_data.get("terms_conditions")
            userProf.save()


            #send confirmation email
            name = user.get_full_name()
            mail_subject = 'Potvrdenie emailu pre MANDALINKU'
            message = render_to_string('home/email_activation_mail.html', {
                'user': name,
                'domain': get_current_site(request).domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
                'protocol': 'https' if request.is_secure() else 'http'
            })
            mail = EmailMessage(mail_subject, message, to=[user.email])

            if mail.send():
                return render(request, "home/confirmation_email_sent.html", {'success': True})
                # mess = f'Dear <b>{name}</b>, please go to you email <b>{email}</b> inbox and click on \
                #     received activation link to confirm and complete the registration. <b>Note:</b> Check your spam folder.'
            else:
                return render(request, "home/confirmation_email_sent.html", {'success': False})
                # mess = f'Problem sending confirmation email to {mail}, check if you typed it correctly.'

    else:
        form = NewUserForm()
    return render(request, "home/new_user.html", {'form': form})

# def new_user_view(request):

#     if request.method == 'POST':
#         form = SignupForm(request.POST)
#         if form.is_valid():
#             email = form.cleaned_data.get('email')
#             user = form.save(commit=False)
#             user.is_active = False
#             user.first_name = form.cleaned_data.get('firstname')
#             user.last_name = form.cleaned_data.get('lastname')
#             user.email = email
#             user.username = user.first_name + \
#                 user.last_name + user.email.split("@")[0]
#             user.save()
#             # username = form.cleaned_data.get('username')
#             # raw_password = form.cleaned_data.get('password1')
#             print(user.id)
#             userProf = UserProfile.objects.get(user_name_id=user.id)
#             userProf.phone = form.cleaned_data.get("phone")
#             userProf.address = form.cleaned_data.get("address")
#             userProf.city = form.cleaned_data.get("city")
#             userProf.district = form.cleaned_data.get("district")
#             userProf.postal = form.cleaned_data.get("postal")
#             userProf.country = form.cleaned_data.get("country")

#             userProf.newsletter = form.cleaned_data.get("newsletter")
#             userProf.terms_conditions = form.cleaned_data.get(
#                 "terms_conditions")

#             if form.cleaned_data.get("food_attr"):
#                 print("food_attr:",form.cleaned_data.get("food_attr"))
#                 userProf.food_preferences.set(
#                     form.cleaned_data.get("food_attr"))
#             if form.cleaned_data.get("food_attr"):
#                 userProf.alergies.set(form.cleaned_data.get("alergies"))
#             userProf.save()
#             username = form.cleaned_data.get("firstname")+" "+form.cleaned_data.get("lastname")
#             #send confirmation email
#             mail_subject = 'Activate your user account.'
#             message = render_to_string('home/template_activate_account.html', {
#                 'user': username,
#                 'domain': get_current_site(request).domain,
#                 'uid': urlsafe_base64_encode(force_bytes(user.pk)),
#                 'token': account_activation_token.make_token(user),
#                 'protocol': 'https' if request.is_secure() else 'http'
#             })
#             mail = EmailMessage(mail_subject, message, to=[email])
#             if mail.send():
#                 mess = f'Dear <b>{username}</b>, please go to you email <b>{email}</b> inbox and click on \
#                     received activation link to confirm and complete the registration. <b>Note:</b> Check your spam folder.'
#             else:
#                 mess = f'Problem sending confirmation email to {mail}, check if you typed it correctly.'

#             return render(request, "home/home.html", {
#                 "message": mark_safe(mess),
#                 "message_type": "success",
#             })

#         for obj in form.fields:
#             field_names = list(form.errors.as_data())
#             print(obj)
#             if obj == "password1" or obj == "password2":
#                 continue
#             elif obj in field_names:
#                 print(obj, form.errors[obj].as_data())
#                 form.fields[obj].widget.attrs["class"] = form.fields[obj].widget.attrs.get(
#                     "class", "") + " is-invalid"
#             else:
#                 form.fields[obj].widget.attrs["class"] = form.fields[obj].widget.attrs.get(
#                     "class", "") + " is-valid"

#     else:
#         form = SignupForm()

#     # print(form.errors)
    
#     districts = [x[0] for x in CityDistrictPostal.objects.values_list("district").distinct()]
#     cities = [x[0] for x in CityDistrictPostal.objects.values_list("city").distinct()]
#     postal_codes = [x[0] for x in CityDistrictPostal.objects.values_list("postal").distinct()]
#     print(postal_codes)
#     streets = Streets.objects.all()
#     return render(request, 'home/new_user.html',
#                     {'form': form,
#                      'districts': districts,
#                      'cities': cities,
#                      'postal_codes': postal_codes,
#                      'streets': streets
#     })


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.generate_future_orders()
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


def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "home/password/password_reset_email.txt"
                    c = {
                    "email": user.email,
                    'domain': '127.0.0.1:8000',
                    'site_name': 'Website',
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "user": user,
                    'token': default_token_generator.make_token(user),
                    'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'admin@example.com',
                                  [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    return redirect("/password_reset/done/")
            else:  # email not in our database
                password_reset_form.fields["email"].widget.attrs["class"] = "form-control opacity-75 rounded-2 shadow is-invalid"
                return render(request=request, template_name="home/password/password_reset.html", 
                    context={"password_reset_form":password_reset_form})
    password_reset_form = PasswordResetForm()
    password_reset_form.fields["email"].widget.attrs["class"] = "form-control opacity-75 rounded-2 shadow"
    password_reset_form.fields["email"].widget.attrs["placeholder"] = "Email"

    return render(request=request, template_name="home/password/password_reset.html", 
        context={"password_reset_form":password_reset_form})

@login_required
def my_account_view(request):
    if request.method == "POST":
        form = EditProfile(request.POST)
        if form.is_valid():
            # Tu treba pridať uloženie zmenených dát
            return HttpResponseRedirect(reverse('home:home'))
        else:
            pass

            
    districts = [x[0] for x in CityDistrictPostal.objects.values_list("district").distinct()]
    cities = [x[0] for x in CityDistrictPostal.objects.values_list("city").distinct()]
    postal_codes = [x[0] for x in CityDistrictPostal.objects.values_list("postal").distinct()]
    print(postal_codes)
    streets = Streets.objects.all()
    
    context = {
        "form": EditProfile(
            initial={
                'firstname': request.user.first_name,
                'lastname': request.user.last_name,
                'email': request.user.email,
                'phone': request.user.profile.phone,
                'newsletter': request.user.profile.newsletter,
                'terms_conditions': request.user.profile.terms_conditions,
                'food_attributes': request.user.profile.food_preferences.all(),
                'alergies': request.user.profile.alergies.all(),
                'street': request.user.profile.street, 
                'house_no': request.user.profile.house_no,
                'district': request.user.profile.district,
                'city': request.user.profile.city,
                'postal': request.user.profile.postal,
                'country': request.user.profile.country,
            }
        ),
        'districts': districts,
        'cities': cities,
        'postal_codes': postal_codes,
        'streets': streets
    }
    
    return render(request,"home/my_account.html",context)

@login_required
def edit_order_view(request):
    if request.method == 'PUT':
        body = json.loads(request.body)
        sleep(.2) # Artificially slow the response to work on placeholders
        recipe_order = RecipeOrderInstance.objects.get(id=body['recipe_id'])
        recipe_order.portions = body['new_amount']
        recipe_order.save()
        return HttpResponse(status=200)
    return HttpResponseBadRequest()

@login_required
def toggle_pickup_view(request):
    body = json.loads(request.body)
    if request.method == 'PUT':
        order = Order.objects.get(id=body['order_id'])
        order.toggle_pickup()
        return JsonResponse({'pickup':order.pickup})
    return HttpResponseBadRequest()