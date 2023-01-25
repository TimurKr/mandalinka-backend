from django.shortcuts import render
from django.http import HttpResponseBadRequest

from accounts.forms import LoginForm

# Create your views here.
def home_page_view(request):
    return render(request, 'customers/pages/home_page.html', {'loginform': LoginForm()})