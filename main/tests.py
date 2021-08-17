from django.urls import resolve
from django.http import HttpRequest
from django.test import TestCase
from . import views


class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve("/")
        self.assertEqual(found.func, views.home_page)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = views.home_page(request)
        html = response.content.decode("utf8")
        self.assertTrue(html.startswith("<html>"))
        self.assertIn("<title>Connect Social Network</title>", html)
        self.assertTrue(html.endswith("</html>"))