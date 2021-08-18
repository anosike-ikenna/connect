from django.urls import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.test import TestCase
from . import views


class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve("/")
        self.assertEqual(found.func, views.home_page)

    def test_home_page_returns_correct_html(self):
        response = self.client.get("/")

        self.assertTemplateUsed(response, "main/index.html")

    def test_can_save_a_POST_request(self):
        response = self.client.post("/", data={"new_post": "A new post item"})
        self.assertIn("A new post item", response.content.decode())
        self.assertTemplateUsed(response, "main/index.html")