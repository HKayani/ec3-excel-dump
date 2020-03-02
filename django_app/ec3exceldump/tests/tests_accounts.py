import logging

from django.test import TestCase
from django.core.exceptions import ValidationError
from django.core.files import File
from ec3exceldump.models import Report, Account

logger = logging.getLogger(__name__)

class AccountCase(TestCase):
	fixtures = [ 'valid_accounts', 'invalid_accounts' ]

	def setUp(self):
		report = Report(cover_date='2019-05-01', account_file='does/not/exist', meter_file='exist/not/does')
		report.id = 432
		report.save()
		self.report = report
		pass

	def test_valid_fixture(self):
		report = Report.objects.get(pk=518)
		accounts = Account.objects.filter(report=report)
		for acct in accounts:
			with self.subTest(account_id=acct.id):
				acct.full_clean()
		pass

	def test_invalid_fixture(self):
		report = Report.objects.get(pk=112)
		accounts = Account.objects.filter(report=report)
		for acct in accounts:
			with self.subTest(account_id=acct.id):
				with self.assertRaises(ValidationError):
					acct.full_clean()
		pass

	def test_valid_inline(self):
		valid_accounts = [
			{
				'id': 4320,
				'college': "NYCCT",
				'account_number': "1773934448",
				'billing_period': "2019-05-01",
				'billed_amount': 999999999.99,
				'resource_type': 'E',
				'energy_usage': -2147483648,
				'demand_usage': 2147483647
			},
			{
				'id': 4321,
				'college': "NYCCT",
				'account_number': "1773934449",
				'billing_period': "2019-05-01",
				'billed_amount': 100000000.01,
				'resource_type': 'E',
				'energy_usage': 2147483647,
				'demand_usage': -2147483648
			}
		]

		for d in valid_accounts:
			account = Account(report=self.report)
			with self.subTest(account_id=account.id):
				for k, v in d.items():
					setattr(account, k, v)
				account.full_clean()
				account.save()
		pass

	def tearDown(self):
		self.report.delete()
		pass
