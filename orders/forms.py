# -*- coding: utf-8 -*-#
from django.conf import settings
from django import forms
from django.forms.models import inlineformset_factory
from django.forms.widgets import CheckboxSelectMultiple, RadioSelect
from django.contrib.admin.widgets import AdminTimeWidget
from orders.models import PaquetePublicidad, Audios, CHOICES

class PaquetePublicidadForm(forms.ModelForm):
	hora_inicial = forms.TimeField(widget = AdminTimeWidget)
	hora_fin = forms.TimeField(widget = AdminTimeWidget)

	pautar_en = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)
	
	class Meta:
		model = PaquetePublicidad
		
class AudiosForm(forms.ModelForm):
	
	class Meta:
		model = Audios
		
		
AudiosFormSet = inlineformset_factory(PaquetePublicidad, Audios, fields=('file',), can_delete=True)