from datetime import datetime

from django.contrib.auth.models import User
from django.db import models
from taggit.managers import TaggableManager
from tinymce.models import HTMLField


class Note(models.Model):
    title = models.CharField(max_length=255)
    body = HTMLField()
    date = models.DateTimeField(default=datetime.now())
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    tags = TaggableManager(blank=True)
    isPrivate = models.BooleanField(default=True)
    uploadedFile = models.FileField(blank=True)

    def __str__(self):
        return f'id {self.id}: {self.title} - {self.date}'

    def get_absolute_url(self):
        return '/'