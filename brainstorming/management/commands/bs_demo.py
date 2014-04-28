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
        'title': u'',
        'text': u'Go Surfing',
        'creator_name': u'Chris',
        'color': IDEA_COLORS[0],
        'image': ''
    },
    {
        'title': u'',
        'text': u'Have a Potluck',
        'creator_name': u'Chris',
        'color': IDEA_COLORS[0],
        'image': 'idea2.jpg'
    },
    {
        'title': u'ForestJump',
        'text': u"Let's go up the Trees!",
        'creator_name': u'Adrian',
        'color': IDEA_COLORS[1],
        'image': 'idea3.jpg'
    },
    {
        'title': u'Gold Prospector',
        'text': u"Gold panning",
        'creator_name': u'Dan',
        'color': IDEA_COLORS[2],
        'image': 'idea4.jpg'
    },
    {
        'title': u'River Boat Trip',
        'text': u"Two boats, one team, tons of beer!",
        'creator_name': u'Adrian',
        'color': IDEA_COLORS[1],
        'image': 'idea5.jpg'
    },
    {
        'title': u'',
        'text': u"BIG BBQ",
        'creator_name': u'Dan',
        'color': IDEA_COLORS[2],
        'image': 'idea6.jpg'
    },
    {
        'title': u'cooking with Kumar',
        'text': u"We are all cooking a great ayurvedan buffet. Then we are inviting all our family members and eat together. Let's meet on another level!",
        'creator_name': u'Pascal',
        'color': IDEA_COLORS[3],
        'image': 'idea7.jpg'
    },
    {
        'title': u'Team goes outdoor',
        'text': u"Outdoor-Event with the whole team!",
        'creator_name': u'Pascal',
        'color': IDEA_COLORS[3],
        'image': 'idea8.jpg'
    },
    {
        'title': u"hike'n'cheese",
        'text': u"We go hiking in the alps and high above the sea of clouds we are trying this delicious alp cheese",
        'creator_name': u'Pascal',
        'color': IDEA_COLORS[3],
        'image': 'idea9.jpg'
    },
    {
        'title': u"Wine and Champagne Tasting",
        'text': u"Enjoy wine and champagne after a relaxing walk...",
        'creator_name': u'',
        'color': IDEA_COLORS[4],
        'image': 'idea10.jpg'
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