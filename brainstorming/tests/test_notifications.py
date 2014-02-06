from brainstorming.models import Brainstorming, BrainstormingWatcher, EmailVerification
from brainstorming.notifications import toggle_notification
from brainstorming.tests.factories import BrainstormingFactory
from brainstorming.views import notification
from brainstorming.viewsets import BrainstormingViewSet
from django.test import RequestFactory
from rest_framework.test import APIRequestFactory
import unittest2
from django.core import mail


class NotificationTestCase(unittest2.TestCase):
    def test_notification_action(self):
        obj = BrainstormingFactory()
        view = BrainstormingViewSet.as_view({'post': 'notification'})
        factory = APIRequestFactory()
        request = factory.post('', {'email': 'test@example.com'}, format='json')
        response = view(request, pk=obj.pk)
        response.render()
        self.assertEqual(response.content, '{"status": "add"}')

    def test_watcher(self):
        creator_email = 'creator@example.com'
        watcher_email = 'watcher@example.com'
        factory = RequestFactory()
        bs = Brainstorming.objects.create(creator_email=creator_email, question='Wat?')

        # Creator is a watcher by default
        self.assertTrue(BrainstormingWatcher.objects.filter(email=creator_email, brainstorming=bs).exists())

        # Add another watcher
        mail.outbox = []
        toggle_notification(bs, watcher_email)
        self.assertEqual(len(mail.outbox), 1)

        verification = EmailVerification.objects.get(email=watcher_email).pk
        request = factory.get('test?ev={0}'.format(verification))
        request.session = {}
        notification(request, bs.pk)
        self.assertTrue(BrainstormingWatcher.objects.filter(email=watcher_email, brainstorming=bs).exists(),
                        'BrainstormingWatcher entry missing')

        # Remove watcher
        mail.outbox = []
        toggle_notification(bs, watcher_email)
        self.assertEqual(len(mail.outbox), 1)

        verification = EmailVerification.objects.get(email=watcher_email).pk
        request = factory.get('test?ev={0}'.format(verification))
        request.session = {}
        notification(request, bs.pk)
        self.assertFalse(BrainstormingWatcher.objects.filter(email=watcher_email, brainstorming=bs).exists(),
                        'BrainstormingWatcher entry still there')

        bs.delete()