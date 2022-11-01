import json
from re import I
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
            user.is_email_valid = True
            user.save()
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
            address = form.save()
            if request.user.addresses.all().count() == 0:
                request.user.addresses.add(address)
        except ValueError:
            pass
        else:
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
        if plan is '0':
            return HttpResponseRedirect(reverse('customers:home_page'))
        elif plan is '1':
            return render(request,"accounts/new_user/pages/set_payment.html")
    return render(request,"accounts/new_user/pages/choose_plan.html")
        


# ACCOUNT MANAGEMENT ##############################################################

@login_required
def my_account_view(request):
    return HttpResponseBadRequest(request)


@login_required
def edit_preferences(request):
    return HttpResponseBadRequest(request)
