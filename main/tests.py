from django.urls import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.test import TestCase
from . import views
from .models import TimeLine


class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve("/")
        self.assertEqual(found.func, views.home_page)

    def test_home_page_returns_correct_html(self):
        response = self.client.get("/")

        self.assertTemplateUsed(response, "main/index.html")

    def test_can_save_a_POST_request(self):
        response = self.client.post("/", data={"new_post": "A new post item"})

        self.assertEqual(TimeLine.objects.count(), 1)
        new_item = TimeLine.objects.first()
        self.assertEqual(new_item.text, "A new post item")

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/')
        # self.assertIn("A new post item", response.content.decode())
        # self.assertTemplateUsed(response, "main/index.html")

    def test_only_saves_items_when_necessary(self):
        self.client.get("/")
        self.assertEqual(TimeLine.objects.count(), 0)

    def test_displays_all_timeline_items(self):
        TimeLine.objects.create(text="item1")
        TimeLine.objects.create(text="item2")

        response = self.client.get("/")

        self.assertIn("item1", response.content.decode())
        self.assertIn("item2", response.content.decode())

    # def test_displays_all_timeline_items_by_asc_created(self):
    #     first = TimeLine.objects.create(text="first")
    #     second = TimeLine.objects.create(text="second")
        
    #     response = self.client.get("/")
    #     posts = None
    #     for context in response.context:
    #         posts = context.get("posts", "")
    #         if posts:
    #             break
    #     print(TimeLine.objects.count(), "*****************")
    #     print(posts.values_list("created"))
    #     print(TimeLine.objects.values_list("created"))
    #     self.assertEqual(
    #         sorted(list(posts.values_list("created"))),
    #         sorted(list(TimeLine.objects.values_list("created")), reverse=True)
    #     )


class TimeLineModelTest(TestCase):

    def test_saving_and_retrieving_items(self):
        first_item = TimeLine()
        first_item.text = "The first (ever) timeline item"
        first_item.save()

        second_item = TimeLine()
        second_item.text = "Item the second"
        second_item.save()

        saved_items = TimeLine.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, "The first (ever) timeline item")
        self.assertEqual(second_saved_item.text, "Item the second")