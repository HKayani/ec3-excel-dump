from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator

# Create your models here.

ELE = 'E'
GAS = 'G'
STM = 'S'
RTC = [
	(ELE, 'Electric'),
	(GAS, 'Gas'),
	(STM, 'Steam')
]
RESOURCE_TYPE_CHOICES = dict(RTC)
	
class Report(models.Model):
	cover_date = models.DateField()
	add_date = models.DateTimeField(auto_now_add=True)
	account_file = models.FileField(upload_to='uploads/accounts/')
	account_file_progress = models.IntegerField(default=0)
	account_file_crawled = models.BooleanField(default=False)
	account_crawl_result = models.IntegerField(default=0)
	account_crawl_msg = models.CharField(max_length=128)
	meter_file = models.FileField(upload_to='uploads/meters/')
	meter_file_progress = models.IntegerField(default=0)
	meter_file_crawled = models.BooleanField(default=False)
	meter_crawl_result = models.IntegerField(default=0)
	meter_crawl_msg = models.CharField(max_length=128)

	def hex_account_crawl(self):
		return hex(self.account_crawl_result)

	def hex_meter_crawl(self):
		return hex(self.meter_crawl_result)

	def __str__(self):
		return str(self.cover_date)

class Account(models.Model):
	report = models.ForeignKey(Report, on_delete=models.CASCADE)
	included = models.BooleanField(default=True)
	college = models.CharField(max_length=256, null=True)
	account_number = models.CharField(max_length = 64, null=True)
	billing_period = models.DateField(null=True) 
	billed_amount = models.DecimalField(max_digits=11, decimal_places=2, null=True)
	resource_type = models.CharField(
		max_length = 1,
		choices = RTC,
		default = ELE,
	)
	energy_usage = models.IntegerField(null=True)
	demand_usage = models.IntegerField(null=True)

	def clean(self):
		# SELF VALIDATION
		if not str(self.account_number).isdigit():
			raise ValidationError("account_number isn't all digits")
		pass

	def get_resource_type(self):
		return RESOURCE_TYPE_CHOICES[self.resource_type]
	
class Meter(models.Model):
	report = models.ForeignKey(Report, on_delete=models.CASCADE)
	account = models.ForeignKey(Account, null=True, on_delete=models.CASCADE)
	included = models.BooleanField(default=True)
	meter_number = models.CharField(max_length=64, null=True)
	energy_usage = models.IntegerField(null=True)
	demand_usage = models.IntegerField(null=True)

	def clean(self):
		# SELF VALIDATION
		if not str(self.meter_number).isdigit():
			raise ValidationError("meter_number isn't all digits")
		pass

class RowIssue(models.Model):
	report = models.ForeignKey(Report, on_delete=models.CASCADE)
	account = models.ForeignKey(Account, null=True, on_delete=models.CASCADE)
	meter = models.ForeignKey(Meter, null=True, on_delete=models.CASCADE)
	excel_row = models.IntegerField()
	message = models.CharField(max_length=256)

	def list_issues(self):
		issues = self.message.split('\n')
		for i in range(len(issues)):
			issues[i] = "<li>" + issues[i] + "</li>"
		issues = ''.join(issues)
		return "<div>" + issues + "</div>"

class Building(models.Model):
	meter = models.ForeignKey(Meter, on_delete=models.CASCADE)
	building_name = models.CharField(max_length=100)
	square_footage = models.IntegerField(default=0)