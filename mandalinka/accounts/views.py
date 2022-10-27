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

from .forms import NewUserForm
from .models import User
from .tokens import account_activation_token


# Create your views here.

def new_user_view(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)

        if form.is_valid():
            try:
                user = form.save()
            except ValueError:
                return render(request, "accounts/pages/new_user.html", {'form': form})

            #send confirmation email
            mail_subject = 'Potvrdenie emailu pre MANDALINKU'
            message = render_to_string('accounts/emails/email_activation.txt', {
                'name': user.first_name,
                'pronoun': user.pronoun,
                'domain': get_current_site(request).domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
                'protocol': 'https' if request.is_secure() else 'http'
            })

            if EmailMessage(mail_subject, message, to=[user.email]).send():
                return render(request, "accounts/pages/email_activation_sent.html", {
                    'name': user.first_name,
                    'pronoun': user.pronoun,
                })
            else:
                user.delete()
                form.add_error('email', ValidationError(
                    _('Na zadanú emailovú adresu sa nám nepodarilo odoslať mail. \
                    Skontrolujte správnosť adresy alebo skúste neskôr.')
                , code='invalid_email'))

    else:
        form = NewUserForm()
    return render(request, "accounts/pages/new_user.html", {'form': form})

