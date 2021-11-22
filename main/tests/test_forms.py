from django.test import TestCase
# from django.core.files import File
from io import BytesIO
from django.core.files.uploadedfile import SimpleUploadedFile
from . import create_user, create_fake_user
from ..models import *
from ..forms import PostForm, EMPTY_POST_ERROR
from unittest import skip
import os


class PostFormTest(TestCase):

    def test_form_validation_for_blank_items(self):
        form = PostForm({"text": ""})
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["text"],
            [EMPTY_POST_ERROR]
        )

    def test_form_save_handles_saving_to_a_timeline(self):
        user = create_user()
        timeline = TimeLine.objects.create(user=user)
        form = PostForm(data={"text": "do me"})
        new_post = form.save(for_timeline=timeline)
        self.assertEqual(new_post, Post.objects.first())
        self.assertEqual(new_post.text, "do me")
        self.assertEqual(new_post.timeline, timeline)

    def test_form_accepts_post_image(self):
        user = create_user()
        timeline = TimeLine.objects.create(user=user)

        img_path = os.path.normpath("c:/users/ikenna/pictures/test2.jpg")

        image_data = {"image": SimpleUploadedFile("test.jpg", open(img_path, "rb").read())}
        form = PostForm({"text": "do me"}, image_data)
        new_post = form.save(for_timeline=timeline)

        self.assertEqual(new_post, Post.objects.first())
        self.assertEqual(new_post.text, "do me")
        self.assertEqual(new_post.timeline, timeline)
        self.assertEqual(os.path.basename(new_post.image.name), "test.jpg")
        new_post.image.delete()