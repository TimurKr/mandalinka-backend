# pages/urls.py
from django.urls import path


# from .views import HomePageView
from . import views

app_name = 'home'

urlpatterns = [
    path("", views.home, name="home"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),

    path("new_user", views.new_user_view, name="new_user"),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),

    path("password_reset", views.password_reset_request, name="password_reset"),
    path('reset/<uidb64>/<token>/', views.PasswordResetSetView.as_view(), name='password_reset_set'),
    path('reset/done/', views.PasswordResetCompleteView.as_view(), name='password_reset_complete'), 
    
    path("my_account", views.my_account_view, name="my_account"),
    path("edit_order", views.edit_order_view, name="edit_order"),
    path("toggle_pickup", views.toggle_pickup_view, name="toggle_pickup"),
]
