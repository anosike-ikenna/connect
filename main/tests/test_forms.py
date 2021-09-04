from django.test import TestCase
from ..models import *
from ..forms import PostForm, EMPTY_POST_ERROR
from unittest import skip


class PostFormTest(TestCase):

    def test_form_validation_for_blank_items(self):
        form = PostForm({"text": ""})
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["text"],
            [EMPTY_POST_ERROR]
        )

    def test_form_save_handles_saving_to_a_timeline(self):
        timeline = TimeLine.objects.create()
        form = PostForm(data={"text": "do me"})
        new_post = form.save(for_timeline=timeline)
        self.assertEqual(new_post, Post.objects.first())
        self.assertEqual(new_post.text, "do me")
        self.assertEqual(new_post.timeline, timeline)