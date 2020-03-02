import logging

from django.test import TestCase

logger = logging.getLogger(__name__)

class SomeTestCase(TestCase):
	def setUp(self):
		self.msg = "This is a message"
		self.num = 2 + 3
		pass

	def test_something(self):
		pass

	def test_otherthing(self):
		self.assertNotEqual(self.num, 6)
		pass