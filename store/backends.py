from django.contrib.auth.backends import BaseBackend
from django.db import OperationalError

from .models import User


class EmailAuthBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        email = kwargs.get('email') or email or kwargs.get('username')
        if not email or not password:
            return None

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return None
        except OperationalError:
            return None

        if user.check_password(password):
            if not hasattr(user, 'backend'):
                user.backend = f"{self.__class__.__module__}.{self.__class__.__name__}"
            return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
        except OperationalError:
            return None
