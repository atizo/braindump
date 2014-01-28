from brainstorming.serializers import BrainstormingSerializer
from brainstorming.tests.factories import BrainstormingFactory
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
