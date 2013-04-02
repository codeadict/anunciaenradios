# -*- coding: utf-8 -*-#
from __future__ import with_statement

from django import forms
from django.conf import settings
from estaciones.models import Estacion, Provincia, Cliente
import datetime
from django.utils.datetime_safe import date
from haystack.forms import FacetedSearchForm
from django.forms.widgets import CheckboxSelectMultiple
from haystack.query import SQ
import operator


class ContactForm(forms.Form):
    """
    Formulario de Contacto
    """
    name = forms.CharField(label='Nombre')
    company = forms.CharField(label='Empresa')
    email = forms.EmailField(label='E-mail')
    phone = forms.CharField(label='Teléfono')
    message = forms.CharField(label='Mensaje', widget=forms.Textarea)
    
class BuscarEstacionForm(FacetedSearchForm):
	regiones = forms.MultipleChoiceField(required=False, 
                                    widget=CheckboxSelectMultiple(), 
                                    choices=Provincia.REGION,)
	edades_target = forms.MultipleChoiceField(required=False, 
                                    widget=CheckboxSelectMultiple(), 
                                    choices=Estacion.NET)
	niveles_socioeconomicos = forms.MultipleChoiceField(required=False, 
                                    widget=CheckboxSelectMultiple(), 
                                    choices=Estacion.NSE)

	def __init__(self, *args, **kwargs):
		super(BuscarEstacionForm, self).__init__(*args, **kwargs)

	def search(self):
		# First, store the SearchQuerySet received from other processing.
		filter_regiones, filter_edad_target, filter_nivel_socioeconomico  = None, None, None
		sqs = super(BuscarEstacionForm, self).search()
		if self.is_valid() and self.cleaned_data['regiones']:
			filter_regiones = [SQ(regiones__exact=str(region)) for region in self.cleaned_data['regiones']]
		if self.is_valid() and self.cleaned_data['edades_target']:
			filter_edad_target = [SQ(edad_target__exact=str(edad_target)) for edad_target in self.cleaned_data['edades_target']]
		if self.is_valid() and self.cleaned_data['niveles_socioeconomicos']:
			filter_nivel_socioeconomico = [SQ(nivel_socioeconomico__exact=str(nivel_socioeconomico)) for nivel_socioeconomico in self.cleaned_data['niveles_socioeconomicos']]
		
		if filter_regiones:
			sqs = sqs.filter_and(reduce(operator.or_, filter_regiones))
		if filter_edad_target:
			sqs = sqs.filter_and((reduce(operator.or_, filter_edad_target)))
		if filter_nivel_socioeconomico:
			sqs = sqs.filter_and((reduce(operator.or_, filter_nivel_socioeconomico)))
		return sqs.highlight()

class ClienteForm(forms.ModelForm):
	class Meta:
		model = Cliente

	def clean_ruc(self):
		if self.cleaned_data['ruc'] != 10:
			raise forms.ValidationError("Debe introducir un número de RUC válido")
