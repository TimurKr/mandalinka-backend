from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns = [
    # New user
    path('new_user', views.new_user_view, name="new_user"),
]