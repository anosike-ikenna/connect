from django.urls import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.test import TestCase
from django.utils.html import escape
from django.contrib.auth import get_user_model
from . import create_user, create_fake_user
from .. import views
from ..models import TimeLine, Post
from ..forms import EMPTY_POST_ERROR, PostForm

User = get_user_model()

class BaseViewTest(TestCase):

    @staticmethod
    def force_login(fn):
        def modified_fn(*args, **kwargs):
            user = create_user()
            self = args[0]
            self.client.force_login(user)
            fn(*args, **kwargs)
        return modified_fn


class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve("/")
        self.assertEqual(found.func, views.home_page)

    def test_home_page_returns_correct_html(self):
        response = self.client.get("/")

        self.assertTemplateUsed(response, "main/index.html")

    def test_can_save_a_POST_request(self):
        user = create_user()
        self.client.force_login(user)
        response = self.client.post("/", data={"text": "A new post item"})

        self.assertEqual(TimeLine.objects.count(), 1)
        new_post = Post.objects.first()
        self.assertEqual(new_post.text, "A new post item")

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'/timeline/')

    def test_only_saves_posts_when_necessary(self):
        self.client.get("/")
        self.assertEqual(TimeLine.objects.count(), 0)

    def test_displays_all_timeline_posts(self):
        user = create_user()
        timeline = TimeLine.objects.create(user=user)
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
        user = create_user()
        timeline = TimeLine.objects.create(user=user)
        self.client.force_login(user)
        response = self.client.get(f"/timeline/")
        self.assertContains(response, "oops! Your timeline is currently empty")

    def test_invalid_post_items_arent_saved(self):
        self.client.post("/", data={"text": ""})
        self.assertEqual(TimeLine.objects.count(), 0)
        self.assertEqual(Post.objects.count(), 0)

    def test_invalid_post_input_renders_home_template(self):
        response = self.client.post("/", data={"text": ""})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "main/index.html")

    @BaseViewTest.force_login
    def test_validation_errors_are_shown_on_home_page(self):
        response = self.client.post("/", data={"text": ""})
        self.assertContains(response, escape(EMPTY_POST_ERROR))

    def test_for_invalid_input_passes_form_to_template(self):
        response = self.client.post("/", data={"text": ""})
        self.assertIsInstance(response.context["form"], PostForm)


class TimeLineViewTest(TestCase):

    def test_uses_timeline_list_template(self):
        user = create_user()
        timeline = TimeLine.objects.create(user=user)
        self.client.force_login(user)
        response = self.client.get(f"/timeline/")
        self.assertTemplateUsed(response, "main/timeline.html")

    def test_displays_only_posts_for_that_timeline(self):
        correct_user = create_user()
        correct_timeline = TimeLine.objects.create(user=correct_user)
        Post.objects.create(text="post1", timeline=correct_timeline)
        Post.objects.create(text="post2", timeline=correct_timeline)
        other_user = create_fake_user()
        other_timeline = TimeLine.objects.create(user=other_user)
        Post.objects.create(text="other timeline post1", timeline=other_timeline)
        Post.objects.create(text="other timeline post2", timeline=other_timeline)

        self.client.force_login(correct_user)
        response = self.client.get(f"/timeline/")

        self.assertContains(response, "post1")
        self.assertContains(response, "post2")
        self.assertNotContains(response, "other timeline post1")
        self.assertNotContains(response, "other timeline post2")

    def test_passes_correct_timeline_to_template(self):
        correct_user = create_user()
        other_user = create_fake_user()
        other_timeline = TimeLine.objects.create(user=other_user)
        correct_timeline = TimeLine.objects.create(user=correct_user)
        self.client.force_login(correct_user)
        response = self.client.get(f"/timeline/")
        self.assertEqual(response.context["timeline"], correct_timeline)

    def test_passes_correct_user_posts_to_template(self):
        email = "alice@test.com"
        username = "alice"
        user = User.objects.create(username=username, email=email)
        alice_timeline = TimeLine.objects.create(user=user)
        Post.objects.create(text="post1", timeline=alice_timeline)
        Post.objects.create(text="post2", timeline=alice_timeline)
        false_user = User.objects.create(username="joker", email="joker@test.com")
        false_timeline = TimeLine.objects.create(user=false_user)
        Post.objects.create(text="joker post1", timeline=false_timeline)
        Post.objects.create(text="joker post2", timeline=false_timeline)

        self.client.force_login(user)
        response = self.client.get("/timeline/")
        
        self.assertContains(response, "post1")
        self.assertContains(response, "post2")
        self.assertNotContains(response, "joker post1")
        self.assertNotContains(response, "joker post2")

    def test_can_save_a_POST_request_to_an_existing_timeline(self):
        correct_user = create_user()
        other_user = create_fake_user()
        other_timeline = TimeLine.objects.create(user=other_user)
        correct_timeline = TimeLine.objects.create(user=correct_user)

        self.client.force_login(correct_user)
        self.client.post(
            f"/timeline/",
            data={"text": "A new post for an existing timeline"}
        )

        self.assertEqual(Post.objects.count(), 1)
        new_post = Post.objects.first()
        self.assertEqual(new_post.text, "A new post for an existing timeline")
        self.assertEqual(new_post.timeline, correct_timeline)

    def test_POST_redirects_to_list_view(self):
        correct_user = create_user()
        other_user = create_fake_user()
        other_timeline = TimeLine.objects.create(user=other_user)
        correct_timeline = TimeLine.objects.create(user=correct_user)

        self.client.force_login(correct_user)
        response = self.client.post(
            f"/timeline/",
            data={"text": "A new post for an existing timeline"}
        )

        self.assertRedirects(response, f"/timeline/")

    def post_invalid_input(self):
        user = create_user()
        timeline = TimeLine.objects.create(user=user)
        self.client.force_login(user)
        return self.client.post(
            f"/timeline/",
            data={"text": ""}
        )

    def test_for_invalid_input_nothing_saved_to_db(self):
        self.post_invalid_input()
        self.assertEqual(Post.objects.count(), 0)

    def test_for_invalid_input_renders_list_template(self):
        response = self.post_invalid_input()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "main/timeline.html")

    def test_for_invalid_input_passes_form_to_template(self):
        response = self.post_invalid_input()
        self.assertIsInstance(response.context["form"], PostForm)

    def test_for_invalid_input_shows_error_on_page(self):
        response = self.post_invalid_input()
        self.assertContains(response, escape(EMPTY_POST_ERROR))