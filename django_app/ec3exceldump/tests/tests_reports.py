import logging
import timeit
import datetime

from django.test import TestCase
from django.core.files import File
from ec3exceldump.models import Report, Account, Meter
from ec3exceldump.views import loadbooks, logger

# logger = logging.getLogger(__name__)

class ReportCase(TestCase):
	def setUp(self):
		account_file = File(open('django_app/ec3exceldump/tests/valid_accounts.xlsx', 'rb'))
		meter_file = File(open('django_app/ec3exceldump/tests/valid_meters.xlsx', 'rb'))
		report = Report(cover_date='2019-5-1', account_file=account_file, meter_file=meter_file)
		report.id = 1200
		report.save()
		self.report = report
		pass

	def test_creation(self):
		report = Report.objects.get(pk=1200)
		self.assertIsNotNone(report)

		self.assertEqual(report.cover_date, datetime.date(2019, 5, 1))
		self.assertTrue(report.account_file.name.startswith('uploads/accounts/'))
		self.assertTrue(report.meter_file.name.startswith('uploads/meters/'))
		pass

	def test_loadbooks(self):
		report = Report.objects.get(pk=1200)
		disableLogging = True

		self.assertEqual(report.account_file_progress, 0)
		self.assertFalse(report.account_file_crawled)
		self.assertEqual(report.account_crawl_result, 0)

		self.assertEqual(report.meter_file_progress, 0)
		self.assertFalse(report.meter_file_crawled)
		self.assertEqual(report.meter_crawl_result, 0)

		logger.disabled = disableLogging
		start_time = timeit.default_timer()
		loadbooks(report.account_file, report.meter_file, report.id)
		elapsed = timeit.default_timer() - start_time
		logger.disabled = not disableLogging
		# logger.warning("loadbooks in " + str(int(elapsed * 1000) / 1000) + "s")
		self.assertTrue(elapsed < 60)

		report = Report.objects.get(pk=1200)

		self.assertEqual(report.account_file_progress, 10000)
		self.assertTrue(report.account_file_crawled)
		self.assertEqual(report.account_crawl_result, 1)

		self.assertEqual(report.meter_file_progress, 10000)
		self.assertTrue(report.meter_file_crawled)
		self.assertEqual(report.meter_crawl_result, 1)

		# The reason it's capped at 10,000 is because when dividing by 100,
		# we can get two decimal places;
		# 000.00 -> 100.00
		# 00,000 -> 10,000

		self.assertGreater(Account.objects.filter(report=report).count(), 0)
		self.assertGreater(Meter.objects.filter(report=report).count(), 0)
		pass

	def tearDown(self):
		self.report.delete()
		pass