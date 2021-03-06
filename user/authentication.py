from main.models import TimeLine
from user.models import User, Token
from . import utils


class PasswordlessAuthenticationBackend:
    
    def authenticate(self, request, uid):
        try:
            token = Token.objects.get(uid=uid)
            if utils.get_custom_datetime() > token.expires:
                token.delete()
                return None
            return User.objects.get(email=token.email)
        except Token.DoesNotExist:
            return None
        except User.DoesNotExist:
            user = User.objects.create(
                email=token.email,
                username=token.username
            )
            TimeLine.objects.create(user=user)
            return user

    def get_user(self, user_id):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None