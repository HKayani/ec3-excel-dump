import logging

from django.test import TestCase
from django.core.exceptions import ValidationError
from django.core.files import File
from ec3exceldump.models import Report, Account, Meter

logger = logging.getLogger(__name__)

class MeterCase(TestCase):
	fixtures = [ 'valid_meters', 'invalid_meters' ]

	def test_valid_fixture(self):
		account = Account.objects.get(pk=1920)
		meters = Meter.objects.filter(account=account)
		for mtr in meters:
			with self.subTest(meter_id=mtr.id):
				mtr.full_clean()
		pass

	def test_invalid_fixture(self):
		account = Account.objects.get(pk=2470)
		meters = Meter.objects.filter(account=account)
		for mtr in meters:
			with self.subTest(meter_id=mtr.id):
				with self.assertRaises(ValidationError):
					mtr.full_clean()
		pass