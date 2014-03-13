import os
import random
from django.conf import settings

from django.db.models import F

import re
from braindump.env import get_full_url
from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django_extensions.db.models import TimeStampedModel


CHARSET = '123456789abcdefghjkmnpqrstvwxzy'
LENGTH = 12
MAX_TRIES = 1024

RED = '#f9846a'
ORANGE = '#ffc95e'
YELLOW = '#f1f44e'
GREEN = '#c9eb5d'
BLUE = '#87d6e4'
TURQUOISE = '#92e5c9'

IDEA_COLORS = [RED, ORANGE, YELLOW, GREEN, BLUE, TURQUOISE]

IDEA_COLORS_CODES = {
    RED: 'c1',
    ORANGE: 'c2',
    YELLOW: 'c3',
    GREEN: 'c4',
    BLUE: 'c5',
    TURQUOISE: 'c6'
}


class Brainstorming(TimeStampedModel):
    id = models.SlugField(primary_key=True, editable=False, blank=True)
    question = models.CharField(max_length=200)
    creator_email = models.EmailField()
    creator_ip = models.CharField(max_length=100, blank=True)
    details = models.TextField(blank=True)

    def __unicode__(self):
        return u'{question} ({id})'.format(question=self.question, id=self.id)

    def save(self, *args, **kwargs):
        loop_num = 0
        while not self.id:
            if loop_num < MAX_TRIES:
                newid = ''.join(random.sample(CHARSET, LENGTH))
                if not Brainstorming.objects.filter(pk=newid).exists():
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
        from brainstorming.notifications import new_brainstorming

        BrainstormingWatcher.objects.create(brainstorming=instance, email=instance.creator_email)
        new_brainstorming(instance)


def get_upload_to(path):
    if settings.DEBUG:
        return os.path.join('uploads/', path)
    return path


class Idea(TimeStampedModel):
    brainstorming = models.ForeignKey('brainstorming.Brainstorming', unique=False)
    title = models.CharField(max_length=200, blank=True)
    text = models.TextField()
    creator_name = models.CharField(max_length=200, blank=True)
    creator_ip = models.CharField(max_length=100, blank=True)
    ratings = models.IntegerField(default=0)
    color = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to=get_upload_to('images'), null=True)

    def rate(self):
        self.ratings = F('ratings') + 1
        self.save()

    def unrate(self):
        self.ratings = F('ratings') - 1
        self.save()

    class Meta:
        ordering = ['-created']


@receiver(post_delete, sender=Idea)
def remove_files(sender, instance=None, **kwargs):
    if instance.image:
        instance.image.delete(False)


class BrainstormingWatcher(TimeStampedModel):
    brainstorming = models.ForeignKey('brainstorming.Brainstorming', unique=False)
    email = models.EmailField()

    class Meta:
        unique_together = (("brainstorming", "email"),)
        ordering = ['-created']


class EmailVerification(TimeStampedModel):
    id = models.SlugField(primary_key=True, editable=False, blank=True)
    email = models.EmailField()

    def save(self, *args, **kwargs):
        loop_num = 0
        while not self.id:
            if loop_num < MAX_TRIES:
                newid = ''.join(random.sample(CHARSET, LENGTH))
                if not EmailVerification.objects.filter(pk=newid).exists():
                    self.id = newid
                loop_num += 1
            else:
                raise ValueError("Couldn't generate a unique code.")

        super(EmailVerification, self).save(*args, **kwargs)

    class Meta:
        ordering = ['-created']