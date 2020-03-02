from django import forms
from .models import Report

class ReportForm(forms.ModelForm):
	class Meta:
		model = Report
		fields = ['cover_date', 'account_file', 'meter_file']