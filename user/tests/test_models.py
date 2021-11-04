from django.test import TestCase
from django.contrib import auth
from user.models import Token

User = auth.get_user_model()


class UserModelTest(TestCase):
    
    def test_user_is_valid_with_email_and_username_only(self):
        user = User(email="alice@test.com", username="alice")
        user.full_clean()
    
    def test_no_problem_with_auth_login(self):
        user = User.objects.create(email="alice@test.com", username="alice")
        user.backend = ""
        request = self.client.request().wsgi_request
        auth.login(request, user)   # should not raise


class TokenModelTest(TestCase):

    def test_links_user_with_auto_generated_uid(self):
        token1 = Token.objects.create(email="alice@test.com", username="alice")
        token2 = Token.objects.create(email="alice@test.com", username="alice")
        self.assertNotEqual(token1.uid, token2.uid)