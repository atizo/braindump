import random

from django.utils.html import strip_tags
import os
from django.conf import settings
from django.db.models import F
import re
from braindump.env import get_full_url
from django.db import models, transaction
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

IDEA_COLOR_CHOICES = [
    (RED, 'RED'),
    (ORANGE, 'ORANGE'),
    (YELLOW, 'YELLOW'),
    (GREEN, 'GREEN'),
    (BLUE, 'BLUE'),
    (TURQUOISE, 'TURQUOISE')
]

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
    idea_sequence = models.IntegerField(default=0)

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

    def disable_url(self):
        return get_full_url('{}/{}'.format(self.pk, 'notification'))

    def get_safe_question(self):
        """
        Transform text links to prevent them from being linkified by mail clients
        """
        return re.sub(r'http(s)?://(www\.)?', '', strip_tags(self.question))

    class Meta:
        ordering = ['-created']


@receiver(post_save, sender=Brainstorming)
def brainstorming_init(sender, instance, created, **kwargs):
    if created:
        from brainstorming.notifications import new_brainstorming

        BrainstormingWatcher.objects.create(brainstorming=instance, email=instance.creator_email)
        new_brainstorming(instance)


def path_and_rename(path):
    if settings.DEBUG:
        path = os.path.join('uploads/', path)

    def wrapper(instance, filename):
        ext = filename.split('.')[-1]
        loop_num = 0
        filename = None
        while not filename:
            if loop_num < MAX_TRIES:
                newid = ''.join(random.sample(CHARSET, LENGTH))
                if not Idea.objects.filter(image__iendswith=newid).exists():
                    filename = newid
                loop_num += 1
            else:
                raise ValueError("Couldn't generate a unique code.")

        # return the whole path to the file
        return os.path.join(path, '{}.{}'.format(newid, ext))

    return wrapper


class Idea(TimeStampedModel):
    brainstorming = models.ForeignKey('brainstorming.Brainstorming', unique=False)
    title = models.CharField(max_length=200, blank=True)
    text = models.TextField()
    creator_name = models.CharField(max_length=200, blank=True)
    creator_ip = models.CharField(max_length=100, blank=True)
    ratings = models.IntegerField(default=0)
    color = models.CharField(max_length=100, blank=True, choices=IDEA_COLOR_CHOICES)
    image = models.ImageField(upload_to=path_and_rename('images'), null=True)
    number = models.IntegerField(default=0)

    def rate(self):
        self.ratings = F('ratings') + 1
        self.save()

    def unrate(self):
        self.ratings = F('ratings') - 1
        self.save()

    def get_safe_text(self):
        """
        Transform text links to prevent them from being linkified by mail clients
        """
        return re.sub(r'http(s)?://(www\.)?', '', strip_tags(self.text))

    def get_absolute_url(self):
        return self.brainstorming.get_absolute_url()

    def __unicode__(self):
        return u'{text} ({number})'.format(text=self.text[:20], number=self.number)

    class Meta:
        ordering = ['-created']


@receiver(post_save, sender=Idea)
def idea_init(sender, instance, created, **kwargs):
    if created:
        with transaction.atomic():
            instance.brainstorming.idea_sequence = F('idea_sequence') + 1
            instance.brainstorming.save()
            instance.number = Brainstorming.objects.get(pk=instance.brainstorming.pk).idea_sequence
            instance.save()


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