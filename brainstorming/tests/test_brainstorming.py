import sys
from brainstorming.serializers import BrainstormingSerializer
from brainstorming.tests.factories import BrainstormingFactory
import unittest2


class BrainstormingTestCase(unittest2.TestCase):
    def test_write_only_email_field(self):
        object = BrainstormingFactory()
        serializer = BrainstormingSerializer(object)
        self.assertNotIn('creatorEmail', serializer.data)
