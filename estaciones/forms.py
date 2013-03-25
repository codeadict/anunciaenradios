# -*- coding: utf-8 -*-#
from __future__ import with_statement

from django import forms
from django.conf import settings

class ContactForm(forms.Form):
    """
    Formulario de Contacto
    """
    name = forms.CharField(label='Nombre')
    company = forms.CharField(label='Empresa')
    email = forms.EmailField(label='E-mail')
    phone = forms.CharField(label='Teléfono')
    message = forms.CharField(label='Mensaje', widget=forms.Textarea)
    
    