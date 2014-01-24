from django.db import models
from django_extensions.db.models import TimeStampedModel

import random

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
