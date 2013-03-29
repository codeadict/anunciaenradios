# -*- coding: utf-8 -*-#
from __future__ import with_statement

from django.http import HttpResponseRedirect, Http404
from django.views.generic import FormView, TemplateView, DetailView

from estaciones.forms import ContactForm
from estaciones.models import Estacion

class ContactView(FormView):
    form_class = ContactForm
    
    def get_initial(self):
        initial = super(ContactView, self).get_initial()       
        return initial
    
    def form_valid(self, form):
        target_url = form.save()
        return HttpResponseRedirect(target_url)

class EstacionDetailView(DetailView):
	model = Estacion
