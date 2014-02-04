import random
import re

from braindump.env import get_full_url
from brainstorming.notifications import new_brainstorming
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_extensions.db.models import TimeStampedModel


CHARSET = '123456789abcdefghjkmnpqrstvwxzy'
LENGTH = 12
MAX_TRIES = 1024


class Brainstorming(TimeStampedModel):
    id = models.SlugField(primary_key=True, editable=False, blank=True)
    question = models.CharField(max_length=200)
    creator_email = models.EmailField()
    creator_ip = models.CharField(max_length=100, blank=True)
    details = models.TextField(blank=True)

    def __unicode__(self):
        return '{question} ({id})'.format(question=self.question, id=self.id)

    def save(self, *args, **kwargs):
        loop_num = 0
        while not self.id:
            if loop_num < MAX_TRIES:
                newid = ''.join(random.sample(CHARSET, LENGTH))
                if Brainstorming.objects.filter(pk=newid).count() == 0:
                    self.id = newid
                loop_num += 1
            else:
                raise ValueError("Couldn't generate a unique code.")

        super(Brainstorming, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return get_full_url(self.id)

    def get_safe_question(self):
        """
        Transform text links to prevent them from being linkified by mail clients
        """
        return re.sub(r'http(s)?://(www\.)?', '', self.question)

    class Meta:
        ordering = ['-created']


@receiver(post_save, sender=Brainstorming)
def send_new_mail(sender, instance, created, **kwargs):
    if created:
        new_brainstorming(instance)


class Idea(TimeStampedModel):
    brainstorming = models.ForeignKey('brainstorming.Brainstorming', unique=False)
    title = models.CharField(max_length=200, blank=True)
    text = models.TextField()
    creator_name = models.CharField(max_length=200, blank=True)
    creator_ip = models.CharField(max_length=100, blank=True)
    #image = models.ImageField()

    class Meta:
        ordering = ['-created']


class BrainstormingWatcher(TimeStampedModel):
    brainstorming = models.ForeignKey('brainstorming.Brainstorming', unique=False)
    email = models.EmailField()

    class Meta:
        unique_together = (("brainstorming", "email"),)
        ordering = ['-created']
