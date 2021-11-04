from django.test import TestCase
from django.urls import resolve
from django.shortcuts import redirect
from django.conf import settings
from django.contrib.auth import get_user_model
import user.views
from user.models import Token
from unittest.mock import patch, call
from unittest import skip

User = get_user_model()


class SendLoginEmailViewTest(TestCase):

    def test_redirects_to_home_page(self):
        response = self.client.post("/user/send_login_email", data={
            "email": "alice@test.com",
            "username": "alice"
        })
        self.assertRedirects(response, "/")

    def test_sets_when_token_is_to_expire(self):
        username = "alice"
        email = "alice@test.com"
        response = self.client.post("/user/send_login_email", data={
            "email": email,
            "username": username
        })
        token = Token.objects.first()
        self.assertTrue(
            int((token.expires - token.created).total_seconds()) == settings.PASSWORD_RESET_TIMEOUT
        )

    @skip
    def test_sends_mail_to_address_from_post(self):
        self.send_mail_called = False

        def fake_send_mail(subject, body, from_email, to_list):
            self.send_mail_called = True
            self.subject = subject
            self.body = body
            self.from_email = from_email
            self.to_list = to_list

        user.views.send_mail = fake_send_mail

        self.client.post("/user/send_login_email", data={
            "email": "alice@test.com",
            "username": "alice",
        })

        self.assertTrue(self.send_mail_called)
        self.assertEqual(self.subject, "Your login for connect")
        self.assertEqual(self.from_email, "noreply@connect")
        self.assertEqual(self.to_list, ["alice@test.com"])

    def test_creates_token_associated_with_email(self):
        self.client.post("/user/send_login_email", data={
            "email": "alice@test.com",
            "username": "alice"
        })
        token = Token.objects.first()
        self.assertTrue(token.email, "alice@test.com")
        self.assertTrue(token.username, "alice")

    @patch("user.views.send_mail")
    def test_sends_link_to_login_using_token_uid(self, mock_send_mail):
        response = self.client.post("/user/send_login_email", data={
            "email": "alice@test.com",
            "username": "alice"
        })

        token = Token.objects.first()
        expected_url = f"http://testserver/user/login?token={token.uid}"
        (subject, body, from_email, to_list), kwargs = mock_send_mail.call_args
        self.assertIn(expected_url, body)

    @patch("user.views.send_mail")
    def test_sends_mail_to_address_from_post(self, mock_send_mail):
        self.client.post("/user/send_login_email", data={
            "email": "alice@test.com",
            "username": "username"
        })
        self.assertEqual(mock_send_mail.called, True)
        (subject, body, from_email, to_list), kwargs = mock_send_mail.call_args
        self.assertEqual(subject, "Your login link for connect")
        self.assertEqual(from_email, "noreply@connect")
        self.assertEqual(to_list, ["alice@test.com"])

    def test_adds_success_message(self):
        response = self.client.post("/user/send_login_email", data={
            "email": "alice@test.com",
            "username": "alice"
        }, follow=True)
        message = list(response.context["messages"])[0]
        self.assertEqual(
            message.message,
            "Check your email, we've sent you a link you can use to log in"
        )
        self.assertEqual(
            message.tags, "success"
        )


class SignupViewTest(TestCase):

    def test_signup_url_resolves_to_signup_view(self):
        found = resolve("/user/signup/")
        
        self.assertTrue(found.func, user.views.signup)

    def test_signup_page_uses_correct_template(self):
        response = self.client.get("/user/signup/")

        self.assertTemplateUsed(response, "user/signup.html")


class PreLoginTest(TestCase):

    def test_pre_login_url_resolves_to_pre_login_view(self):
        found = resolve("/user/pre_login/")

        self.assertTrue(found.func, user.views.pre_login)

    def test_pre_login_page_uses_correct_template(self):
        response = self.client.get("/user/pre_login/")

        self.assertTemplateUsed(response, "user/pre_login.html")

    def test_returns_login_template_for_non_existent_email(self):
        response = self.client.post("/user/pre_login/", data={
            "email": "alice@test.com"
        })
        self.assertTemplateUsed(response, "user/pre_login.html")

    @patch("user.views.send_login_email")
    def test_calls_send_login_email_if_email_exists(self, mock_send_login_email):
        user_one = User.objects.create(email="alice@test.com", username="alice")
        user_two = User.objects.create(email="tonto@test.com", username="tonto")

        mock_send_login_email.return_value = redirect("/")
        response = self.client.post("/user/pre_login/", data={
            "email": "alice@test.com"
        })

        self.assertTrue(mock_send_login_email.called)

    def test_redirects_to_home_page_if_login_email_sent(self):
        user_one = User.objects.create(email="alice@test.com", username="alice")
        response = self.client.post("/user/pre_login/", data={
            "email": "alice@test.com"
        })
        self.assertRedirects(response, "/")


@patch("user.views.auth")
class LoginViewTest(TestCase):

    def test_redirects_to_home_page(self, mock_auth):
        response = self.client.get("/user/login?token=abcd123")
        self.assertRedirects(response, "/")
    
    def test_calls_authenticate_with_uid_from_get_request(self, mock_auth):
        self.client.get("/user/login?token=abcd123")
        self.assertEqual(
            mock_auth.authenticate.call_args,
            call(uid="abcd123")
        )

    def test_calls_auth_login_with_user_if_there_is_one(self, mock_auth):
        response = self.client.get("/user/login?token=abcd123")
        self.assertEqual(
            mock_auth.login.call_args,
            call(response.wsgi_request, mock_auth.authenticate.return_value)
        )

    def test_does_not_login_if_user_is_not_authenticated(self, mock_auth):
        mock_auth.authenticate.return_value = None
        self.client.get("/user/login?token=abcd123")
        self.assertEqual(mock_auth.login.called, False)