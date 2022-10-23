from re import I
from time import sleep
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseBadRequest, JsonResponse
from django.urls import reverse, reverse_lazy
from django.db.models.query_utils import Q
from django.template.loader import render_to_string
from django.core.mail import send_mail, EmailMessage, BadHeaderError

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import views as auth_views
from django.contrib.sites.shortcuts import get_current_site


from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str

from home.forms import *
from home.models import Order, User
from recepty.models import RecipeOrderInstance
import json
from .tokens import account_activation_token



# Basics ------------------------------------------------------------------------------------------------

def home(request):
    if request.user.is_authenticated:
        context = {}
    else:
        context = {
            "loginform": LoginForm(),
        }
    return render(request, "home/home.html", context)


def login_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('home:home'))

    if request.method == "POST":
        form = LoginForm(request=request, data=request.POST)
        if form.is_valid():
            user = form.get_user(request)

            # If user object is returned, log in and route to index page:
            if user:
                login(request, user)
                return HttpResponseRedirect(reverse("home:home"))
    else:
        form = LoginForm()

    context = {
            "loginform": form,
            "focus": "LoginModal",
        }
    return render(request, "home/home.html", context)


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("home:home"))


# New user creation ----------------------------------------------------------------------------------------

def new_user_view(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)

        if form.is_valid():

            user = form.save()
                
            #send confirmation email
            mail_subject = 'Potvrdenie emailu pre MANDALINKU'
            message = render_to_string('home/new_user/email_activation_mail.txt', {
                'name': user.first_name,
                'pronoun': user.pronoun,
                'domain': get_current_site(request).domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
                'protocol': 'https' if request.is_secure() else 'http'
            })
            mail = EmailMessage(mail_subject, message, to=[user.email])

            if mail.send():
                return render(request, "home/new_user/email_activation_sent.html", context={
                    'name': user.first_name,
                    'pronoun': user.pronoun,
                })
            else:
                logout()
                user.delete()
                form.add_error('email', ValidationError(
                    _('Na zadanú emailovú adresu sa nám nepodarilo odoslať mail. \
                    Skontrolujte správnosť adresy alebo skúste neskôr.')
                , code='invalid_email'))

    else:
        form = NewUserForm()
    return render(request, "home/new_user/create_user.html", {'form': form})

def activate_email(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        return HttpResponseRedirect(reverse('home:home'))
    else:
        if account_activation_token.check_token(user, token):
            user.is_email_valid = True
            user.save()
            login(request, user)
            return render(request, 'home/new_user/email_activation_confirmed.html', context={
                        'name': user.first_name,
                        'pronoun': user.pronoun,
                    })
        else:
            return HttpResponseRedirect(reverse('home:home'))


@login_required
def add_first_address(request):
    if request.method == 'POST':
        form = FirstAddressForm(request.POST)
        try:
            address = form.save()
        except ValueError:
            pass
        else:
            request.user.addresses.add(address)
            return HttpResponseRedirect(reverse('home:add_preferences'))
    else:
        form = FirstAddressForm()
    return render(request,"home/new_user/add_address.html", context={'form':form})

@login_required
def set_preferences(request):
    form = PreferencesForm(request.POST, instance=request.user)
    if request.method == "POST":    
        try:
            form.save()
        except ValueError:
            pass
        else:
            return HttpResponseRedirect(reverse('home:add_first_payment'))
    return render(request,"home/new_user/set_preference.html", {'form', form})




# Password reset --------------------------------------------------------------------------------------------

def password_reset_request(request):
    if request.method == "POST":
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                user = None
            if not user:
                form.add_error(None, ValidationError('Užívateľ neexistuje', 'user_not_in_database'))
                return render(request, "home/password_reset/start.html", 
                    context={"form":form})
            form.send_mail(
                subject_template_name='home/password_reset/email_subject_template.txt',
                email_template_name='home/password_reset/email_body_template.txt',
                context = {
                    'name': user.first_name,
                    'pronoun': user.pronoun,
                    'domain': '127.0.0.1:8000',
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': default_token_generator.make_token(user),
                    'protocol':  'http', 
                    },
                from_email = 'admin@example.com',
                to_email = form.cleaned_data['email']
            )
            return render(request, 'home/password_reset/email_sent.html', 
                context={'pronoun': user.pronoun})
    else:
        form = PasswordResetForm()
    return render(request, "home/password_reset/start.html", 
        context={"form":form})

class PasswordResetSetView(auth_views.PasswordResetConfirmView):
    template_name = 'home/password_reset/set.html'
    form_class = SetPasswordForm
    reset_url_token = "set-password"
    success_url = reverse_lazy('home:password_reset_complete')
    title = "Zadajte nové heslo"

class PasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'home/password_reset/complete.html'
    title = 'Heslo zmenené úspešne'


# Account management ---------------------------------------------------------------------------------------

def render_my_account(
    request, 
    general_form: GeneralUserInfoForm = None,
    preferences_form: PreferencesForm = None,
    ):

    general_form = general_form or GeneralUserInfoForm(instance=request.user)
    preferences_form = preferences_form or PreferencesForm(instance=request.user)
    
    addresses = [{
            'id': address.id, 
            'name': address.name, 
            'address': address.address,
            'primary': address.primary,
        } for address in request.user.addresses.all()]

    return render(request,"home/manage/my_account.html",context = {
        'general_form': general_form,
        'addresses': addresses,
        'preferences_form': preferences_form,
    })

@login_required
def my_account_view(request):
    return render_my_account(request)

@login_required
def edit_general(request):
    if request.method == 'POST':
        form = GeneralUserInfoForm(request.POST, instance=request.user)
        try:
            form.save()
        except ValueError:
            return render_my_account(request, general_form=form)
    return HttpResponseRedirect(reverse('home:my_account'))

@login_required
def add_address(request):
    if request.method == 'POST':
        form = AddAddressForm(request.POST)
        try:
            address = form.save()
        except ValueError:
            pass
        else:
            request.user.add_address(address)
            return HttpResponseRedirect(reverse('home:my_account'))
    else:
        form = AddAddressForm()
    return render(request,"home/manage/add_address.html", context={'form':form})

@login_required
def edit_address(request, address_id):
    try:
        address = Address.objects.get(id=address_id)
    except:
        return HttpResponseBadRequest()

    if request.method == 'POST':
        form = EditAddressForm(address_id,request.POST, instance=address)
        try:
            form.save()
        except ValueError:
            pass
        else:
            return HttpResponseRedirect(reverse('home:my_account'))
    else:
        form = EditAddressForm(address_id, instance=address)
        return render(request,"home/manage/edit_address.html", context={'form':form})

@login_required
def delete_address(request, address_id):
    try:
        address = Address.objects.get(id=address_id)
    except:
        return HttpResponseBadRequest()
    address.delete()
    return HttpResponseRedirect(reverse('home:my_account'))
    
@login_required
def set_primary_address(request, address_id):
    try:
        address = Address.objects.get(id=address_id)
    except:
        return HttpResponseBadRequest()
    else:
        address.set_primary()
        return HttpResponseRedirect(reverse('home:my_account'))

@login_required
def edit_preferences(request):
    if request.method == 'POST':
        form = PreferencesForm(request.POST, instance=request.user)
        try:
            form.save()
        except ValueError:
            return render_my_account(request, preferences_form=form)
    return HttpResponseRedirect(reverse('home:my_account'))

# Order APIs -----------------------------------------------------------------------------------------------
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