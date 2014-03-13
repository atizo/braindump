from brainstorming.models import Brainstorming, EmailVerification
from brainstorming.permissions import PERMISSION_MAP, PERMISSION_PROJECT, brainstorming_set_edit_perm, edit_mode
from brainstorming.serializers import BrainstormingSerializer
from brainstorming.tests.factories import BrainstormingFactory
from brainstorming.views import edit
from brainstorming.viewsets import BrainstormingViewSet
from django.conf import settings
from django.contrib.auth.models import User
from django.core import mail
from django.test import RequestFactory
from django.utils.importlib import import_module
from rest_framework import status
from rest_framework.test import APIRequestFactory
import unittest2


class BrainstormingTestCase(unittest2.TestCase):
    def _session(self):
        return import_module(settings.SESSION_ENGINE).SessionStore()

    def test_retrieval(self):
        obj = BrainstormingFactory.build()
        serializer = BrainstormingSerializer(obj)

        # 'creatorEmail' should be write-only
        self.assertEqual(set(['id', 'created', 'question', 'details', 'url', 'canEdit', 'detailsHTML']),
                         set(serializer.data.keys()))

    def test_creation(self):
        serializer = BrainstormingSerializer(data={})
        self.assertFalse(serializer.is_valid())

        serializer = BrainstormingSerializer(data={'question': 'q', 'creatorEmail': 'john@example.org'})
        self.assertTrue(serializer.is_valid())

        serializer = BrainstormingSerializer(data={'question': 'q', 'details': 'd', 'creatorEmail': 'john@example.org'})
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.object.question, 'q')
        self.assertEqual(serializer.object.details, 'd')
        self.assertEqual(serializer.object.creator_email, 'john@example.org')

    def test_permissions(self):
        view = BrainstormingViewSet.as_view({'get': 'list'})
        factory = APIRequestFactory()
        request = factory.get('')

        # Guest can not list brainstormings
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


        # Staff can list brainstormings
        request.user = User(is_staff=True)
        request.session = self._session()
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Guest can post
        view = BrainstormingViewSet.as_view({'post': 'create'})
        request = factory.post('', {'creatorEmail': 'test@example.com', 'question': 'Was?'}, format='json')
        request.session = self._session()
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Guest can not update
        obj = BrainstormingFactory()
        view = BrainstormingViewSet.as_view({'patch': 'partial_update'})
        request = factory.patch('', {'question': 'Aha?'}, format='json')
        request.session = self._session()
        response = view(request, pk=obj.pk).render()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Owner can update
        brainstorming_set_edit_perm(request, obj.pk)

        response = view(request, pk=obj.pk).render()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_edit_mode(self):
        factory = RequestFactory()
        creator_email = 'creator@example.com'
        bs = Brainstorming.objects.create(creator_email=creator_email, question='Wat?')
        mail.outbox = []

        # Only creator can edit
        ret = edit_mode(bs, 'wrong@example.com')
        self.assertEqual(len(mail.outbox), 0)
        self.assertEqual(ret, {'status': 'ban'})

        # Creator edit
        ret = edit_mode(bs, creator_email)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(ret, {'status': 'edit'})

        verification = EmailVerification.objects.get(email=creator_email).pk
        request = factory.get('test?ev={0}'.format(verification))
        request.session = self._session()
        edit(request, bs.pk)

        self.assertTrue(bs.pk in request.session[PERMISSION_MAP][PERMISSION_PROJECT])

        serializer = BrainstormingSerializer(bs, context={'request': request})
        self.assertTrue(serializer.data['canEdit'])

        bs.delete()