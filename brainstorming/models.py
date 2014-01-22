from django.db import models
from django_extensions.db.models import TimeStampedModel


class Brainstorming(TimeStampedModel):
    question = models.CharField(max_length=200)
    details = models.TextField(blank=True)
    creator_email = models.EmailField(blank=True)
    #image = models.ImageField()

    class Meta:
        ordering = ['-created']


class Idea(TimeStampedModel):
    brainstorming = models.ForeignKey('brainstorming.Brainstorming', unique=False)
    title = models.CharField(max_length=200, blank=True)
    text = models.TextField()
    #image = models.ImageField()

    class Meta:
        ordering = ['-created']


class BrainstormingWatcher(TimeStampedModel):
    brainstorming = models.ForeignKey('brainstorming.Brainstorming', unique=False)
    email = models.EmailField()

    class Meta:
        unique_together = (("brainstorming", "email"),)
        ordering = ['-created']
