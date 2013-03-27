# -*- coding: utf-8 -*-#
from __future__ import with_statement

from django import forms
from django.conf import settings
from estaciones.models import Estacion
import datetime
from django.utils.datetime_safe import date

class ContactForm(forms.Form):
    """
    Formulario de Contacto
    """
    name = forms.CharField(label='Nombre')
    company = forms.CharField(label='Empresa')
    email = forms.EmailField(label='E-mail')
    phone = forms.CharField(label='Teléfono')
    message = forms.CharField(label='Mensaje', widget=forms.Textarea)
    
# class EstacionForm(forms.ModelForm):
# 	class Meta:
#         model = Estacion

#     def clean_en_promocion_desde(self):
#     	en_promocion_desde = self.cleaned_data['en_promocion_desde']
    	
