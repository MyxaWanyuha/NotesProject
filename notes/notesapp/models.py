from datetime import datetime

from django.contrib.auth.models import User
from django.db import models


class Note(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    date = models.DateField(default=datetime.now())
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'id {self.id}: {self.title} - {self.date}'
