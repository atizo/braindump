import random

from braindump.env import get_full_url
from brainstorming.notifications import new_brainstorming
from django.core.mail import send_mail
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.defaultfilters import truncatechars
from django.template.loader import render_to_string
from django_extensions.db.models import TimeStampedModel


CHARSET = '123456789abcdefghjkmnpqrstvwxzy'
LENGTH = 12
MAX_TRIES = 1024


class Brainstorming(TimeStampedModel):
    slug = models.SlugField(primary_key=True, editable=False, blank=True)
    question = models.CharField(max_length=200)
    creator_email = models.EmailField()
    details = models.TextField(blank=True)

    def __unicode__(self):
        return '{question} ({slug})'.format(question=self.question, slug=self.slug)

    def save(self, *args, **kwargs):
        loop_num = 0
        while not self.slug:
            if loop_num < MAX_TRIES:
                newslug = ''.join(random.sample(CHARSET, LENGTH))
                if Brainstorming.objects.filter(pk=newslug).count() == 0:
                    self.slug = newslug
                loop_num += 1
            else:
                raise ValueError("Couldn't generate a unique code.")

        super(Brainstorming, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return get_full_url(self.slug)

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
    #image = models.ImageField()

    class Meta:
        ordering = ['-created']


class BrainstormingWatcher(TimeStampedModel):
    brainstorming = models.ForeignKey('brainstorming.Brainstorming', unique=False)
    email = models.EmailField()

    class Meta:
        unique_together = (("brainstorming", "email"),)
        ordering = ['-created']
