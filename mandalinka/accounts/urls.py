from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns = [
    # Basics
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),

    # New user
    path('new_user', views.new_user_view, name='new_user'),
    path('new_user/email_confirmed/<uidb64>/<token>', views.email_confirmed_view, name='email_confirmed'),
    path('new_user/add_address', views.add_first_address_view, name='add_first_address'),
    path('new_user/set_preferences', views.set_preferences_view, name='set_preferences'),
    path('new_user/choose_plan', views.choose_plan_view, name='choose_plan'),

    # Manage account
    path('my_account', views.my_account_view, name='my_account'),
    path('my_account/edit_preferences', views.edit_preferences, name='edit_preferences'),

    # Password reset
    path('password_reset', views.password_reset_request, name='password_reset'),
    path('password_reset/<uidb64>/<token>', views.PasswordResetSetView.as_view(), name='password_reset_set'),
    path('password_reset/complete', views.PasswordResetCompleteView.as_view(), name='password_reset_complete'), 
]