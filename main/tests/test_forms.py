from django.test import TestCase
from ..forms import PostForm, EMPTY_POST_ERROR


class PostFormTest(TestCase):

    def test_form_validation_for_blank_items(self):
        form = PostForm({"text": ""})
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["text"],
            [EMPTY_POST_ERROR]
        )