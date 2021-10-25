from django.test import TestCase
from django.contrib.auth import get_user_model
from django.http import HttpRequest
from user.authentication import PasswordlessAuthenticationBackend
from user.models import Token

User = get_user_model()


class AuthenticateTest(TestCase):

    def test_returns_None_if_no_such_token(self):
        result = PasswordlessAuthenticationBackend().authenticate(
            HttpRequest(),
            "invalid-token"
        )
        self.assertIsNone(result)
    
    def test_returns_new_user_with_correct_email_if_token_exists(self):
        email = "alice@test.com"
        username = "alice"
        token = Token.objects.create(email=email, username=username)
        user = PasswordlessAuthenticationBackend().authenticate(
            HttpRequest(),
            token.uid
        )
        new_user = User.objects.get(email=email)
        self.assertEqual(user, new_user)

    def test_returns_existing_user_with_correct_email_if_token_exists(self):
        email = "alice@test.com"
        username = "alice"
        existing_user = User.objects.create(email=email, username=username)
        token = Token.objects.create(email=email, username=username)
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