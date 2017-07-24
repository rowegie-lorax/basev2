from django.conf import settings
from django.contrib.auth import get_user_model


class EmailOrPhonenumberBackend(object):

    def authenticate(self, username=None, password=None):
        if '@' in username:
            kwargs = {'email': username}
        else:
            kwargs = {'phone_number': username}
        try:
            user = get_user_model().objects.get(**kwargs)
            if user.check_password(password):
                return user
        except get_user_model().DoesNotExist:
            return None

    def get_user(self, username):
        try:
            return get_user_model().objects.get(pk=username)
        except get_user_model().DoesNotExist:
            return None
