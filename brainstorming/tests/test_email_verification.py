from brainstorming.email_verification import get_verified_email, send_email_verification
from brainstorming.models import EmailVerification
from django.core import mail
from django.core.urlresolvers import reverse
from django.test import RequestFactory
import re
import unittest2


class EmailVerificationTestCase(unittest2.TestCase):
    def test_email_verification(self):
        mail.outbox = []

        url = reverse('notification', kwargs={'brainstorming_id': '123456789012'})

        send_email_verification(to='me@example.com',
                                subject='Test',
                                callback=url,
                                template='brainstroming/mails/toggle_notification.txt',
                                context={'action': 'activate'}
        )

        url = 'http://example.com' + url
        body = mail.outbox[0].body
        ev_id = re.search(r'ev=(?P<ev_id>\w{12})', body)

        self.assertEqual(len(mail.outbox), 1)
        self.assertTrue(url in body, '{0} not in email'.format(url))
        self.assertTrue(EmailVerification.objects.filter(pk=ev_id.group('ev_id')).exists(),
                        'Email Verification not found')

    def test_resolve(self):
        email = 'me@axample.com'

        ev = EmailVerification.objects.create(email=email)
        pk = ev.pk
        factory = RequestFactory()

        request = factory.get('test?ev={0}'.format(pk))

        verified_email = get_verified_email(request)
        self.assertFalse(EmailVerification.objects.filter(pk=pk).exists())
        self.assertEqual(verified_email, email)