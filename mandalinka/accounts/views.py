import json
from re import I
import re
from time import sleep
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseBadRequest, JsonResponse
from django.urls import reverse, reverse_lazy
from django.db.models.query_utils import Q
from django.template.loader import render_to_string


from django.core.mail import send_mail, EmailMessage, BadHeaderError
from django.core.exceptions import ValidationError

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import views as auth_views
from django.contrib.sites.shortcuts import get_current_site

from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.utils.translation import gettext_lazy as _

from . import forms
from .models import User, Address
from .tokens import account_activation_token

# BASICS ##################################################################################

def login_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('customers:home_page'))

    if request.method == "POST":
        form = forms.LoginForm(request=request, data=request.POST)
        if form.is_valid():
            user = form.get_user()

            # If user object is returned, log in and route to index page:
            if user:
                login(request, user)
                return HttpResponseRedirect(reverse('customers:home_page'))
    else:
        form = forms.LoginForm()

    context = {
            "loginform": form,
            "focus": "LoginModal",
        }
    return render(request, "customers/pages/home_page.html", context)

@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('customers:home_page'))

# NEW USER ################################################################################

def new_user_view(request):
    if request.method == "POST":
        form = forms.NewUserForm(request.POST)

        if form.is_valid():
            try:
                user = form.save()
            except ValueError:
                pass
            else:
                #send confirmation email
                mail_subject = 'Potvrdenie emailu pre MANDALINKU'
                message = render_to_string('accounts/new_user/emails/email_activation.txt', {
                    'name': user.first_name,
                    'pronoun': user.pronoun,
                    'domain': get_current_site(request).domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                    'protocol': 'https' if request.is_secure() else 'http'
                })

                if EmailMessage(mail_subject, message, to=[user.email]).send():
                    return render(request, "accounts/new_user/pages/activation_email_sent.html", {
                        'name': user.first_name,
                        'pronoun': user.pronoun,
                    })
                else:
                    print(user)
                    user.delete()
                    print(user)
                    form.add_error('', ValidationError(
                        _('Na zadanú emailovú adresu sa nám nepodarilo odoslať mail. \
                        Skontrolujte správnosť adresy alebo skúste neskôr.'), 
                        code='invalid_email'))
                    form.add_error('email', ValidationError(''))

    else:
        form = forms.NewUserForm()
    return render(request, "accounts/new_user/pages/new_user.html", {'form': form})

def email_confirmed_view(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        pass
    else:
        if account_activation_token.check_token(user, token):
            user.validate_email()
            login(request, user)
            return render(request, 'accounts/new_user/pages/email_confirmed.html', context={
                        'name': user.first_name,
                        'pronoun': user.pronoun,
                    })
        
    return HttpResponseRedirect(reverse('customers:home_page'))

@login_required
def add_first_address_view(request):
    if request.method == 'POST':
        form = forms.FirstAddressForm(request.POST)
        try:
            address = form.save(commit=False)
        except ValueError:
            pass
        else:
            address.user = request.user
            address.save()
            return HttpResponseRedirect(reverse('accounts:set_preferences'))
    else:
        form = forms.FirstAddressForm()
    return render(request,"accounts/new_user/pages/add_address.html", context={'form':form})

@login_required
def set_preferences_view(request):
    if request.method == "POST":    
        form = forms.SetPreferencesForm(request.POST, instance=request.user)
        try:
            form.save()
        except ValueError:
            pass
        else:
            return HttpResponseRedirect(reverse('accounts:choose_plan'))
    form = forms.SetPreferencesForm(instance=request.user)
    return render(request,"accounts/new_user/pages/set_preferences.html", {'form': form})

@login_required
def choose_plan_view(request):
    if request.method == 'POST':
        pass
    elif request.method == 'GET':
        plan = request.GET.get('plan', '')
        if plan == '0':
            request.user.save()
            return HttpResponseRedirect(reverse('customers:home_page'))
        elif plan == '1':
            request.user.start_subscription(force=True) #TODO: Remove force when we have working payments
            return render(request,"accounts/new_user/pages/set_payment.html")
    return render(request,"accounts/new_user/pages/choose_plan.html")
        

# ACCOUNT MANAGEMENT ##############################################################

def render_my_account(
    request, section=None,
    general_form: forms.GeneralUserInfoForm = None,
    preferences_form: forms.PreferencesForm = None,
    ):

    general_form = general_form or forms.GeneralUserInfoForm(instance=request.user)
    preferences_form = preferences_form or forms.PreferencesForm(instance=request.user)
    
    addresses = [
        {
            'id': address.id, 
            'name': address.name, 
            'address': address.address,
            'primary': address.primary,
        } for address in request.user.addresses.all().order_by('id')]

    return render(request,"accounts/manage/pages/my_account.html",context = {
        'section': section,
        'general_form': general_form,
        'addresses': addresses,
        'preferences_form': preferences_form,
    })

@login_required
def my_account_view(request, section = None):
    if request.method == 'GET':
        section = request.GET.get('section', None)
    return render_my_account(request, section=section)
        

@login_required
def edit_general(request):
    if request.method == 'POST':
        form = forms.GeneralUserInfoForm(request.POST, instance=request.user)
        try:
            form.save()
        except:
            pass
        else:
            return HttpResponseRedirect(reverse('accounts:my_account')+'?section=general')
    return render_my_account(request, section='general', general_form = form or None)

@login_required
def add_address(request):
    if request.method == 'POST':
        form = forms.AddAddressForm(request.POST)
        try:
            address = form.save(commit=False)
        except ValueError:
            pass
        else:
            if request.user.addresses.filter(name=address.name).count() == 0:
                address.user = request.user
                address.save()
                return HttpResponseRedirect(reverse('accounts:my_account')+'?section=addresses')
            else:
                form.add_error('name', ValidationError('Adresa s daným menom už existuje', 'name_not_unique'))
    else:
        form = forms.AddAddressForm()
    return render(request,"accounts/manage/pages/add_address.html", {'form':form})

@login_required
def edit_address(request, address_id):
    try:
        address = Address.objects.get(id=address_id)
    except:
        return render_my_account(request, section=address)

    if request.method == 'POST':
        form = forms.EditAddressForm(address_id, request.POST, instance=address)
        try:
            address = form.save(commit=False)
        except ValueError:
            pass
        else:
            if request.user.addresses.filter(name=address.name).count() <= 1:
                address.user = request.user
                address.save()
                return HttpResponseRedirect(reverse('accounts:my_account')+'?section=addresses')
            else:
                form.add_error('name', ValidationError('Adresa s daným menom už existuje', 'name_not_unique'))
    else:
        form = forms.EditAddressForm(address_id, instance=address)
    return render(request,"accounts/manage/pages/edit_address.html", {'form':form})

@login_required
def delete_address(request, address_id):
    try:
        address = Address.objects.get(id=address_id)
    except:
        pass
    else:
        address.delete()
    finally:
        return HttpResponseRedirect(reverse('accounts:my_account')+'?section=addresses')

@login_required
def set_primary_address(request, address_id):
    try:
        address = Address.objects.get(id=address_id)
    except:
        pass
    else:
        address.make_primary()
    finally:
        return HttpResponseRedirect(reverse('accounts:my_account')+'?section=addresses')


@login_required
def edit_preferences(request):
    if request.method == 'POST':
        form = forms.PreferencesForm(request.POST, instance=request.user)
        try:
            form.save()
        except:
            pass
        else:
            return HttpResponseRedirect(reverse('accounts:my_account')+'?section=preferences')
    return render_my_account(request, section='preferences', preferences_form = form or None)

class PasswordChangeView(auth_views.PasswordChangeView):
    template_name = 'accounts/manage/pages/password_change.html'
    form_class = forms.PasswordChangeForm
    success_url = reverse_lazy('accounts:my_account')
    title = 'Zmena hesla'


@login_required
def email_change(request):
    return HttpResponseBadRequest(request)

@login_required
def deactivate_account(request):
    return HttpResponseBadRequest(request)

# PASSWORD RESET ###################################################################

def password_reset_request(request):
    if request.method == "POST":
        form = forms.PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
            except:
                form.add_error(None, ValidationError('Užívateľ neexistuje', 'user_not_in_database'))
            else:
                form.send_mail(
                    subject_template_name='accounts/password_reset/emails/subject.txt',
                    email_template_name='accounts/password_reset/emails/body.txt',
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
                return render(request, 'accounts/password_reset/pages/email_sent.html', 
                    context={'pronoun': user.pronoun})
    else:
        form = forms.PasswordResetForm()
    return render(request, "accounts/password_reset/pages/request.html", {"form": form})

class PasswordResetSetView(auth_views.PasswordResetConfirmView):
    template_name = 'accounts/password_reset/pages/set.html'
    form_class = forms.SetPasswordForm
    reset_url_token = 'set-password'
    success_url = reverse_lazy('accounts:password_reset_complete')
    title = 'Zadajte nové heslo'

class PasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'accounts/password_reset/pages/complete.html'
    title = 'Heslo zmenené úspešne'