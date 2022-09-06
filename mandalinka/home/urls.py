# pages/urls.py
from django.urls import path
<<<<<<< HEAD
from . import views

urlpatterns = [
    path("", views.landing_page, name="landing_page"),
=======
from .views import HomePageView
from . import views

app_name = 'home'

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout")
>>>>>>> 5eed795bccf3da02612bfbee7b6f0110a8837eb6
]
