from brainstorming.permissions import PERMISSION_MAP, PERMISSION_PROJECT
from brainstorming.serializers import BrainstormingSerializer
from brainstorming.tests.factories import BrainstormingFactory
from brainstorming.viewsets import BrainstormingViewSet
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIRequestFactory
import unittest2


class BrainstormingTestCase(unittest2.TestCase):
    def test_retrieval(self):
        obj = BrainstormingFactory.build()
        serializer = BrainstormingSerializer(obj)

        # 'creatorEmail' should be write-only
        self.assertEqual(set(['id', 'created', 'question', 'details', 'url']),
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

        # Guest can not list brainstromings
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


        # Staff can list brainstromings
        request.user = User(is_staff=True)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Guest can post
        view = BrainstormingViewSet.as_view({'post': 'create'})
        request = factory.post('', {'creatorEmail': 'test@example.com', 'question': 'Was?'}, format='json')
        request.session = {}
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Guest can not update
        obj = BrainstormingFactory()
        view = BrainstormingViewSet.as_view({'patch': 'partial_update'})
        request = factory.patch('', {'question': 'Aha?'}, format='json')
        request.session = {}
        response = view(request, pk=obj.pk).render()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Owner can update
        request.session = {
            PERMISSION_MAP: {
                PERMISSION_PROJECT: [obj.id]
            }
        }
        response = view(request, pk=obj.pk).render()
        self.assertEqual(response.status_code, status.HTTP_200_OK)