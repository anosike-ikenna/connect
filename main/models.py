from django.db import models
from django.urls import reverse


class TimeLine(models.Model):
    created = models.DateTimeField("date posted", auto_now_add=True)
    last_modified = models.DateTimeField("modified at", auto_now=True)


class Post(models.Model):
    text = models.TextField(default=True, blank=False)
    timeline = models.ForeignKey(TimeLine, default=None, on_delete=models.CASCADE)
    created = models.DateTimeField("date posted", auto_now_add=True)
    last_modified = models.DateTimeField("modified at", auto_now=True)