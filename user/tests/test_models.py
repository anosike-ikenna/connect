from django.test import TestCase
from django.contrib.auth import get_user_model
from user.models import Token

User = get_user_model()


class UserModelTest(TestCase):
    
    def test_user_is_valid_with_email_and_password_only(self):
        user = User(email="test@test.com", username="alice")
        user.full_clean()


class TokenModelTest(TestCase):

    def test_links_user_with_auto_generated_uid(self):
        token1 = Token.objects.create(email="test@test.com", username="alice")
        token2 = Token.objects.create(email="test@test.com", username="alice")
        self.assertNotEqual(token1.uid, token2.uid)
    