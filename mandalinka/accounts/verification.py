# Email verification
# to be able to verify through email as well as password
from django.db import models
from .models import User
from django.core.exceptions import MultipleObjectsReturned
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


class EmailVerification(ModelBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = self.get_user_model()
        try:  # to allow authentication through phone number or any other field, modify the below statement
            user = UserModel.objects.get(
                models.Q(username__iexact=username) | models.Q(email__iexact=username))
        except UserModel.DoesNotExist:
            UserModel().set_password(password)
        except self.MultipleObjectsReturned:
            return User.objects.filter(email=username).order_by('id').first()
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user

    def get_user(self, user_id):
        UserModel = self.get_user_model()
        try:
            user = UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None

        return user if self.user_can_authenticate(user) else None
