from django.db import models
from django.utils import timezone

from event_management.users.models import User


class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateTimeField(default=timezone.now)
    location = models.CharField(max_length=255)
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    attendees = models.ManyToManyField(User, related_name="attendees", blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
