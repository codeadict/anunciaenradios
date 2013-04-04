# -*- coding: utf-8 -*-#
from django.views.generic import FormView, TemplateView, DetailView, ListView 
from django.views.generic.edit import CreateView


from orders.forms import PaquetePublicidadForm
from orders.models import Orden, PaquetePublicidad

from django.http import HttpResponseRedirect



class PaquetePublicidadFormView(CreateView):
    form_class = PaquetePublicidadForm
    model = PaquetePublicidad
    success_url = '/ordenes/mis_paquetes/'

    def post(self, request, *args, **kwargs):
    	#print request.user
    	self.duenno = request.user
    	return super(PaquetePublicidadFormView, self).post(request, *args, **kwargs)

    def form_valid(self, form):
    	self.object = form.save(commit=False)
    	self.object.duenno = self.duenno
    	print self.object.duenno
    	self.object.save()
        return HttpResponseRedirect(self.get_success_url())

class PaquetePublicidadList(ListView):
	model = PaquetePublicidad
	paginate_by = 10

class OrdenList(ListView):
	model = Orden
	paginate_by = 10