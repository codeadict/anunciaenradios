# -*- coding: utf-8 -*-#
from django.views.generic import FormView, TemplateView, DetailView, ListView 
from django.views.generic.edit import CreateView


from anunciaenradios.settings import *
from orders.models import Orden
from orders.forms import CartForm
from django.http import HttpResponseRedirect
from django.contrib.contenttypes.models import ContentType
import uuid


class CartFormView(CreateView):
    form_class = CartForm
    model = Orden
    success_url = '/ordenes/ordenar/'

    def post(self, request, *args, **kwargs):
        self.numero = str(uuid.uuid4());
    	self.cliente = request.user
        product_object = request.POST['product_object']
        meta = product_object.split(':')
        self.object_id = meta[1]
        self.content_type = ContentType.objects.get(pk=meta[0])
        model = self.content_type.get_object_for_this_type(pk=meta[1])
        precio = 0.0
        try:
            precio = model.precio
        except:
            precio = model.precio_nacional#, model.precio_regional?
        self.total_incl_iva = precio # * IVA
        self.cantidad = request.POST['cantidad']
        self.estado = "Pendiente" 
        self.request = request
    	return super(CartFormView, self).post(request, *args, **kwargs)

    def form_valid(self, form):
    	self.object = form.save(commit=False)
    	self.object.cliente = self.cliente
    	self.object.numero = self.numero;
        self.object.total_incl_iva = float(self.total_incl_iva) * float(self.cantidad);
        self.object.estado = self.estado
        self.object.object_id = self.object_id
        self.object.content_type = self.content_type 

    	self.object.save()
        return HttpResponseRedirect(self.get_success_url() + \
                                    "?success=1" + \
                                    "&estacion=" + str(self.request.POST["estacion"]) + \
                                    "&content_type_horarios=" + str(self.request.POST["content_type_horarios"]) + \
                                    "&content_type_paquetes=" + str(self.request.POST["content_type_paquetes"]))

class OrdenList(ListView):
	model = Orden
	paginate_by = 10