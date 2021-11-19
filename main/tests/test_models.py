from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.urls import reverse
from ..models import TimeLine, Post

User = get_user_model()


class TimeLineAndPostModelTest(TestCase):

    def test_timeline_can_have_models(self):
        username = "alice"
        email = "alice@test.com"
        user = User.objects.create(username=username, email=email)
        timeline = TimeLine.objects.create(user=user)
        self.assertEqual(timeline, user.timeline)

    def test_saving_and_retrieving_posts(self):
        username = "alice"
        email = "alice@test.com"
        user = User.objects.create(username=username, email=email)
        timeline = TimeLine(user=user)
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

    def test_cannot_save_empty_post_items(self):
        username = "alice"
        email = "alice@test.com"
        user = User.objects.create(username=username, email=email)
        timeline = TimeLine.objects.create(user=user)
        post = Post(text="", timeline=timeline)
        with self.assertRaises(ValidationError):
            post.full_clean()
            post.save()

    def test_get_absolute_url(self):
        username = "alice"
        email = "alice@test.com"
        user = User.objects.create(username=username, email=email)
        timeline = TimeLine.objects.create(user=user)

        response = timeline.get_absolute_url()
        
        self.assertEqual(reverse("view_timeline"), response)