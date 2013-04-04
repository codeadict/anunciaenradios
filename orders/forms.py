# -*- coding: utf-8 -*-#

from django import forms
from django.forms.widgets import CheckboxSelectMultiple
from orders.models import PaquetePublicidad


class PaquetePublicidadForm(forms.ModelForm):
	class Meta:
		model = PaquetePublicidad