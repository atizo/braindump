from brainstorming.models import Brainstorming, BrainstormingWatcher
from brainstorming.tests.factories import BrainstormingFactory
from brainstorming.viewsets import BrainstormingViewSet
from rest_framework.test import APIRequestFactory
import unittest2


class NotificationTestCase(unittest2.TestCase):
    def test_notification_action(self):
        obj = BrainstormingFactory()
        view = BrainstormingViewSet.as_view({'post': 'notification'})
        factory = APIRequestFactory()
        request = factory.post('', {'email': 'test@example.com'}, format='json')
        response = view(request, pk=obj.pk)
        response.render()
        #self.assertEqual(response.content, '{"status": "updated"}')


    def test_watcher(self):
        creator_email = 'creator@example.com'
        bs = Brainstorming.objects.create(creator_email=creator_email, question='Wat?')

        # Creator is a watcher by default
        self.assertEqual(BrainstormingWatcher.objects.filter(email=creator_email, brainstorming=bs).count(), 1)

        # Add another watcher



        # add watcher
        # email = 'me@axample.com'
        # ev = EmailVerification.objects.create(email=email)
        #
        # pk = ev.pk
        # factory = RequestFactory()
        #
        # request = factory.get('test?ev={0}'.format(pk))
        #
        # verified_email = get_verified_email(request)
        # self.assertEqual(EmailVerification.objects.filter(pk=pk).count(), 0)
        # self.assertEqual(verified_email, email)