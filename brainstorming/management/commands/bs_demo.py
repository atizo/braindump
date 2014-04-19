# -*- coding: utf-8 -*-
from datetime import timedelta
import random

from django.utils import timezone
import os
from brainstorming.models import Brainstorming, Idea, IDEA_COLORS
from django.conf import settings
from django.core.files import File
from django.core.management.base import BaseCommand, CommandError


IDEAS = [
    {
        'title': u'Idee 1',
        'text': u'Lorem Ipsum',
        'creator_name': u'Reto',
        'color': IDEA_COLORS[0],
        'image': ''
    },
    {
        'title': u'',
        'text': u'Alles mit Bild ist gut und schön',
        'creator_name': u'Hans',
        'color': IDEA_COLORS[1],
        'image': 'idea1.jpg'
    },
    {
        'title': u'',
        'text': u'Ne andere mit Bild und Link http://www.noo.com und so',
        'creator_name': u'Fritz',
        'color': IDEA_COLORS[2],
        'image': 'idea2.jpg'
    }
]

IDEA_IMAGE_PATH = os.path.join(settings.BASE_DIR, '../brainstorming/demo')


class Command(BaseCommand):
    help = 'Reset demo brainstorming'

    def handle(self, *args, **options):

        try:
            bs = Brainstorming.objects.get(pk=settings.DEMO_PROJECT)
        except Brainstorming.DoesNotExist:
            raise CommandError('Brainstorming "%s" does not exist' % settings.DEMO_PROJECT)

        bs.question = 'What could we do as a team event?'
        bs.idea_sequence = 0
        bs.save()

        for idea in Idea.objects.filter(brainstorming=bs):
            idea.delete()

        time_offset = 2000
        last_created = len(IDEAS) * time_offset

        for new_idea in IDEAS:
            last_created = random.randint(last_created - time_offset, last_created)
            idea = Idea.objects.create(brainstorming=bs,
                                       created=timezone.now() - timedelta(seconds=last_created),
                                       **new_idea)
            image_name = new_idea['image']
            if len(image_name):
                f = open(os.path.join(IDEA_IMAGE_PATH, image_name))
                idea.image.save(image_name, File(f))
                f.close()

        self.stdout.write('Successfully reset brainstorming "%s"' % settings.DEMO_PROJECT)