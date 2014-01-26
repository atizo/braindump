from django.conf import settings
from django.core.mail import send_mail
from django.template.defaultfilters import truncatechars
from django.template.loader import render_to_string


def new_brainstorming(brainstorming, language=settings.LANGUAGE_CODE):
    send_mail('Link for brainstorming "{0}"'.format(truncatechars(brainstorming.question, 10)),
              render_to_string('brainstroming/mails/new.txt', {'brain': brainstorming}),
              'braindump@heroku.com',
              [brainstorming.creator_email],
              fail_silently=False)