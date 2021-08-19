from django.db import models


class TimeLine(models.Model):
    text = models.TextField(default="")
    created = models.DateTimeField("date posted", auto_now_add=True)
    last_modified = models.DateTimeField("modified at", auto_now=True)