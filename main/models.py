from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class TimeLine(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created = models.DateTimeField("date posted", auto_now_add=True)
    last_modified = models.DateTimeField("modified at", auto_now=True)


class Post(models.Model):
    text = models.TextField()
    timeline = models.ForeignKey(TimeLine, default=None, on_delete=models.CASCADE)
    created = models.DateTimeField("date posted", auto_now_add=True)
    last_modified = models.DateTimeField("modified at", auto_now=True)