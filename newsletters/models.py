from datetime import datetime

from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify


class Tag(models.Model):
    name = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique=True)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name


class Newsletter(models.Model):

    class Frequency(models.IntegerChoices):
        DAILY = 1,
        WEEKLY = 7,
        MONTHLY = 30,

    name = models.CharField(max_length=250)
    description = models.TextField()
    image_url = models.URLField(max_length=250)
    tags = models.ManyToManyField(Tag, related_name="newsletters")
    target = models.IntegerField(default=10)
    votes = models.ManyToManyField(User, related_name="newsletters_voted", blank=True)
    published = models.BooleanField(default=False)
    published_at = models.DateField(null=True)
    frequency = models.IntegerField(choices=Frequency.choices, default=Frequency.WEEKLY)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    created_by = models.ForeignKey(User, related_name="newsletters_created", on_delete=models.SET_NULL, null=True)
    subscribers = models.ManyToManyField(User, related_name="subscriptions", blank=True)

    def __str__(self):
        return self.name
