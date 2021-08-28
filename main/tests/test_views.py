from django.urls import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.test import TestCase
from django.utils.html import escape
from .. import views
from ..models import TimeLine, Post


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
        new_post = Post.objects.first()
        self.assertEqual(new_post.text, "A new post item")

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'/{new_post.timeline.id}/timeline/')

    def test_only_saves_posts_when_necessary(self):
        self.client.get("/")
        self.assertEqual(TimeLine.objects.count(), 0)

    def test_displays_all_timeline_posts(self):
        timeline = TimeLine.objects.create()
        Post.objects.create(text="post1", timeline=timeline)
        Post.objects.create(text="post2", timeline=timeline)

        response = self.client.get("/")

        self.assertIn("post1", response.content.decode())
        self.assertIn("post2", response.content.decode())

    # def test_displays_all_timeline_posts_by_asc_created(self):
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


class NewTimeLineTest(TestCase):
    
    def test_timeline_is_empty_on_get(self):
        timeline = TimeLine.objects.create()
        response = self.client.get(f"/{timeline.id}/timeline/")
        self.assertContains(response, "oops! Your timeline is currently empty")

    def test_validation_errors_are_sent_back_to_home_page_template(self):
        response = self.client.post("/", data={"new_post": ""})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "main/index.html")
        expected_error = "You can't have an empty post"
        self.assertEqual(response.context["error"], expected_error)
        self.assertContains(response, escape(expected_error))

    def test_invalid_post_items_arent_saved(self):
        self.client.post("/", data={"new_post": ""})
        self.assertEqual(TimeLine.objects.count(), 0)
        self.assertEqual(Post.objects.count(), 0)


class TimeLineViewTest(TestCase):

    def test_uses_timeline_list_template(self):
        timeline = TimeLine.objects.create()
        response = self.client.get(f"/{timeline.id}/timeline/")
        self.assertTemplateUsed(response, "main/timeline.html")

    def test_displays_only_posts_for_that_timeline(self):
        correct_timeline = TimeLine.objects.create()
        Post.objects.create(text="post1", timeline=correct_timeline)
        Post.objects.create(text="post2", timeline=correct_timeline)
        other_timeline = TimeLine.objects.create()
        Post.objects.create(text="other timeline post1", timeline=other_timeline)
        Post.objects.create(text="other timeline post2", timeline=other_timeline)

        response = self.client.get(f"/{correct_timeline.id}/timeline/")

        self.assertContains(response, "post1")
        self.assertContains(response, "post2")
        self.assertNotContains(response, "other timeline post1")
        self.assertNotContains(response, "other timeline post2")

    def test_passes_correct_timeline_to_template(self):
        other_timeline = TimeLine.objects.create()
        correct_timeline = TimeLine.objects.create()
        response = self.client.get(f"/{correct_timeline.id}/timeline/")
        self.assertEqual(response.context["timeline"], correct_timeline)


class NewPostTest(TestCase):
    
    def test_can_save_a_POST_request_to_an_existing_timeline(self):
        other_timeline = TimeLine.objects.create()
        correct_timeline = TimeLine.objects.create()

        self.client.post(
            f"/{correct_timeline.id}/timeline/add_post",
            data={"new_post": "A new post for an existing timeline"}
        )

        self.assertEqual(Post.objects.count(), 1)
        new_post = Post.objects.first()
        self.assertEqual(new_post.text, "A new post for an existing timeline")
        self.assertEqual(new_post.timeline, correct_timeline)

    def test_redirects_to_list_view(self):
        other_timeline = TimeLine.objects.create()
        correct_timeline = TimeLine.objects.create()

        response = self.client.post(
            f"/{correct_timeline.id}/timeline/add_post",
            data={"new_post": "A new post for an existing timeline"}
        )

        self.assertRedirects(response, f"/{correct_timeline.id}/timeline/")