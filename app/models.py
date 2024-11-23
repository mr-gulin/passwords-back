from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    name = models.CharField(default="", blank=True, null=True, max_length=255)
    google_picture = models.URLField(blank=True, null=True, max_length=255)
