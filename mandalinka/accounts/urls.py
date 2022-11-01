from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns = [
    # New user
    path('new_user', views.new_user_view, name="new_user"),
    path('new_user/email_confirmed/<uidb64>/<token>', views.email_confirmed_view, name="email_confirmed"),
    path('new_user/add_address', views.add_first_address_view, name="add_first_address"),
    path('new_user/set_preferences', views.set_preferences_view, name="set_preferences"),
    path('new_user/choose_plan', views.choose_plan_view, name="choose_plan"),


    # Manage account
    path('my_account', views.my_account_view, name="my_account"),
    path('my_account', views.edit_preferences, name="edit_preferences"),
]