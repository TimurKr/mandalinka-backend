from django.views.generic import TemplateView
from django.shortcuts import render
from recepty.models import Recipe

    # Create your views here.
def landing_page(request):
    return render(request, "home/landing_page.html", {
        "recipes": Recipe.objects.all(),
    })