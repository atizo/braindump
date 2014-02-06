from brainstorming.email_verification import send_email_verification
from brainstorming.models import BrainstormingWatcher
from django.conf import settings
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.template.defaultfilters import truncatechars
from django.template.loader import render_to_string


def new_brainstorming(brainstorming, language=settings.LANGUAGE_CODE):
    send_mail(u'Link for brainstorming "{0}"'.format(truncatechars(brainstorming.get_safe_question(), 20)),
              render_to_string('brainstroming/mails/new.txt', {'brain': brainstorming}),
              settings.FORM_MAIL,
              [brainstorming.creator_email],
              fail_silently=False)


def toggle_notification(brainstorming, email):
    url = reverse('notification', kwargs={'brainstorming_id': brainstorming.pk})
    status = 'add'
    action = 'activate'
    subject = 'Activate brainstroming notifications'

    if BrainstormingWatcher.objects.filter(brainstorming=brainstorming, email=email).exists():
        status = 'remove'
        action = 'deactivate'
        subject = 'Deactivate brainstroming notifications'

    send_email_verification(to=email,
                            subject=subject,
                            callback=url,
                            template='brainstroming/mails/toggle_notification.txt',
                            context={'action': action, 'brain': brainstorming}
    )

    return {'status': status}