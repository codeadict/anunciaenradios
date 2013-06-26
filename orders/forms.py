# -*- coding: utf-8 -*-#
from django.conf import settings
from django import forms
from django.forms.models import inlineformset_factory
from django.forms.widgets import CheckboxSelectMultiple, RadioSelect
from django.contrib.admin.widgets import AdminTimeWidget, AdminDateWidget
from orders.models import PaquetePublicidad, Audios, HorariosPautas, CHOICES

class PaquetePublicidadForm(forms.ModelForm):
	hora_inicial = forms.TimeField(widget = AdminTimeWidget)
	hora_fin = forms.TimeField(widget = AdminTimeWidget)

	pautar_en = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)
	
	class Meta:
		model = PaquetePublicidad
		
class AudiosForm(forms.ModelForm):
	
	class Meta:
		model = Audios
		
class HorariosPautasForm(forms.ModelForm):
	fecha = forms.DateField(widget = AdminDateWidget(attrs={'class': 'dtField'}))
	
	class Meta:
		model = Audios
	
		
		
AudiosFormSet = inlineformset_factory(PaquetePublicidad, Audios, fields=('file',), can_delete=True)

HorariosFormSet = inlineformset_factory(PaquetePublicidad, HorariosPautas, fields=('fecha','cantidad',), form=HorariosPautasForm, can_delete=True)