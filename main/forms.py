from django import forms
from .models import Post

EMPTY_POST_ERROR = "You can't have an empty post"


class PostForm(forms.ModelForm):
    
    class Meta:
        model = Post
        exclude = ("timeline",)
        error_messages = {
            "text": {"required": EMPTY_POST_ERROR}
        }

    def save(self, for_timeline):
        self.instance.timeline = for_timeline
        return super().save()