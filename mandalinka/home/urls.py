# pages/urls.py
from django.urls import path

# from .views import HomePageView
from . import views

app_name = 'home'

urlpatterns = [
    path("", views.index, name="home"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("new_user", views.new_user_view, name="new_user"),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path("password_reset", views.password_reset_request, name="password_reset"),
    path("my_account", views.my_account_view, name="my_account"),
]
