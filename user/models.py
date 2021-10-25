from django.db import models
from django.utils import timezone
import uuid


class User(models.Model):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30, unique=True)

    REQUIRED_FIELDS = []
    USERNAME_FIELD = "email"
    is_anonymous = True
    is_authenticated = False


class Token(models.Model):
    email = models.EmailField()
    username = models.CharField(max_length=30)
    uid = models.CharField(default=uuid.uuid4, max_length=40)
    created = models.DateTimeField(auto_now_add=True)
    expires = models.DateTimeField(default=timezone.now)