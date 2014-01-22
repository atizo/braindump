import sys
from brainstorming.serializers import BrainstormingSerializer
from brainstorming.tests.factories import BrainstormingFactory
import unittest2


class BrainstormingTestCase(unittest2.TestCase):
    def test_write_only_email_field(self):
        obj = BrainstormingFactory.build()
        serializer = BrainstormingSerializer(obj)
        self.assertNotIn('creatorEmail', serializer.data)
