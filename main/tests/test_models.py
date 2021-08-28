from django.test import TestCase
from django.core.exceptions import ValidationError
from ..models import TimeLine, Post


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

    def test_cannot_save_empty_post_items(self):
        timeline = TimeLine.objects.create()
        post = Post(text="", timeline=timeline)
        with self.assertRaises(ValidationError):
            post.full_clean()
            post.save()