from django.test import TestCase
from django.urls import resolve
import user.views
from user.models import Token
from unittest.mock import patch
from unittest import skip


class SendLoginEmailViewTest(TestCase):

    def test_redirects_to_home_page(self):
        response = self.client.post("/user/send_login_email", data={
            "email": "alice@test.com",
            "username": "alice"
        })
        self.assertRedirects(response, "/")

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

        print(type(response.context))
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


class LoginViewTest(TestCase):

    def test_redirects_to_home_page(self):
        response = self.client.get("/user/login?token=abcd123")
        self.assertRedirects(response, "/")