from django.test import TestCase
from django.contrib.auth import get_user_model
from django.http import HttpRequest
from django.conf import settings
from django.utils import timezone
from main.models import TimeLine
from user.authentication import PasswordlessAuthenticationBackend, utils
from user.models import Token
from unittest import skip
from unittest.mock import patch
import datetime

User = get_user_model()


class AuthenticateTest(TestCase):

    def test_returns_None_if_no_such_token(self):
        result = PasswordlessAuthenticationBackend().authenticate(
            HttpRequest(),
            "invalid-token"
        )
        self.assertIsNone(result)

    @patch("user.utils.get_custom_datetime")
    def test_returns_None_if_token_is_expired(self, mock_utils_datetime):
        username = "alice"
        email = "alice@test.com"
        token = Token.objects.create(email=email, username=username)
        token.expires = token.created + datetime.timedelta(
            seconds=settings.PASSWORD_RESET_TIMEOUT
        )
        token.save()
        mock_utils_datetime.return_value = token.expires + datetime.timedelta(seconds=1)
        result = PasswordlessAuthenticationBackend().authenticate(
            HttpRequest(),
            token.uid
        )
        self.assertIsNone(result)

    @patch("user.utils.get_custom_datetime")
    def test_deletes_token_if_is_expired(self, mock_utils_datetime):
        username = "alice"
        email = "alice@test.com"
        token = Token.objects.create(email=email, username=username)
        token.expires = token.created + datetime.timedelta(
            seconds=settings.PASSWORD_RESET_TIMEOUT
        )
        token.save()
        self.assertEqual(str(token.uid), str(Token.objects.first().uid))
        self.assertEqual(Token.objects.count(), 1)

        mock_utils_datetime.return_value = token.expires + datetime.timedelta(seconds=1)
        result = PasswordlessAuthenticationBackend().authenticate(
            HttpRequest(),
            token.uid
        )

        self.assertIsNone(result)
        self.assertEqual(Token.objects.count(), 0)

    
    def test_returns_new_user_with_correct_email_if_token_exists(self):
        email = "alice@test.com"
        username = "alice"
        token = Token.objects.create(email=email, username=username)
        token.expires = token.created + datetime.timedelta(
            seconds=settings.PASSWORD_RESET_TIMEOUT
        )
        token.save()
        user = PasswordlessAuthenticationBackend().authenticate(
            HttpRequest(),
            token.uid
        )
        new_user = User.objects.get(email=email)
        self.assertEqual(user, new_user)

    def test_creates_timeline_for_new_user_if_token_exists(self):
        email = "alice@test.com"
        username = "alice"
        token = Token.objects.create(email=email, username=username)
        token.expires = token.created + datetime.timedelta(
            seconds=settings.PASSWORD_RESET_TIMEOUT
        )
        token.save()
        user = PasswordlessAuthenticationBackend().authenticate(
            HttpRequest(),
            token.uid
        )
        new_user = User.objects.get(email=email)
        new_user_timeline = TimeLine.objects.get(user=new_user)
        self.assertEqual(new_user_timeline.user, new_user)
        

    def test_returns_existing_user_with_correct_email_if_token_exists(self):
        email = "alice@test.com"
        username = "alice"
        existing_user = User.objects.create(email=email, username=username)
        token = Token.objects.create(email=email, username=username)
        token.expires = token.created + datetime.timedelta(
            seconds=settings.PASSWORD_RESET_TIMEOUT
        )
        token.save()
        user = PasswordlessAuthenticationBackend().authenticate(
            HttpRequest(),
            token.uid
        )
        self.assertEqual(user, existing_user)


class GetUserTest(TestCase):

    def test_gets_user_by_id(self):
        User.objects.create(email="crap@test.com", username="crap")
        correct_user = User.objects.create(
            email="alice@test.com",
            username="alice"
        )
        found_user = PasswordlessAuthenticationBackend().get_user(
            correct_user.id
        )
        self.assertEqual(found_user, correct_user)

    def test_returns_None_if_no_user_with_that_email(self):
        self.assertIsNone(
            PasswordlessAuthenticationBackend().get_user(55)
        )