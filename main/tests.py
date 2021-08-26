from django.urls import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.test import TestCase
from . import views
from .models import TimeLine, Post


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


class TimeLineAndPostModelTest(TestCase):

    def test_saving_and_retrieving_posts(self):
        timeline = TimeLine()
        timeline.save()

        first_post = Post()
        first_post.text = "My first post item"
        first_post.timeline = timeline
        first_post.save()

        second_post = Post()
        second_post.text = "My second post item"
        second_post.timeline = timeline
        second_post.save()

        saved_timeline = TimeLine.objects.first()
        self.assertEqual(saved_timeline, timeline)

        saved_posts = Post.objects.all()
        self.assertEqual(saved_posts.count(), 2)

        first_saved_post = saved_posts[0]
        second_saved_post = saved_posts[1]
        self.assertEqual(first_saved_post.text, "My first post item")
        self.assertEqual(second_saved_post.text, "My second post item")
        self.assertEqual(first_saved_post.timeline, timeline)
        self.assertEqual(second_saved_post.timeline, timeline)


class NewTimeLineTest(TestCase):
    
    def test_timeline_is_empty_on_get(self):
        timeline = TimeLine.objects.create()
        response = self.client.get(f"/{timeline.id}/timeline/")
        self.assertContains(response, "oops! Your timeline is currently empty")


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