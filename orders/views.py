# -*- coding: utf-8 -*-#
from django.views.generic import FormView, TemplateView, DetailView, ListView 
from django.views.generic.edit import CreateView


from orders.forms import PaquetePublicidadForm
from orders.models import Orden, PaquetePublicidad
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect
import uuid


class PaquetePublicidadFormView(CreateView):
    form_class = PaquetePublicidadForm
    model = PaquetePublicidad

    def post(self, request, *args, **kwargs):
    	self.numero = str(uuid.uuid4())
        self.duenno = request.user

        self.object_ids = []
        self.content_types = []
        self.cantidades = []
        self.totales = []

        self.success_url = request.POST['success_url']
        product_object_cantidades = request.POST['product_object_cantidad'].split('|')[:-1]
        for product_object_cant in product_object_cantidades:
            meta = product_object_cant.split(':')
            self.object_ids.append(meta[1])
            content_type = ContentType.objects.get(pk=meta[0])
            self.content_types.append(content_type)
            model = content_type.get_object_for_this_type(pk=meta[1])
            self.cantidades.append(meta[2])

            precio = 0.0
            try:
                precio = model.precio
            except:
                precio = model.precio_nacional#, model.precio_regional?
            self.totales.append(precio) # * IVA
        
        self.estado = "Pendiente"
        self.request = request
        return super(PaquetePublicidadFormView, self).post(request, *args, **kwargs)

    def form_valid(self, form):
    	self.object = form.save(commit=False)
    	self.object.duenno = self.duenno
        #Campos del model Orden
        self.object.save()

        # Salvar las ordenes multimples:
        for i in range(len(self.cantidades)):
            object_id = self.object_ids[i]
            content_type = self.content_types[i]
            cantidad = self.cantidades[i]
            total = self.totales[i]
            orden = Orden(numero=self.numero,
                        cliente=self.duenno,
                        total_incl_iva=float(total) * float(cantidad),
                        estado=self.estado,
                        object_id=object_id,
                        content_type=content_type,
                        cantidad=cantidad,
                        paquete_publicidad=self.object)
            orden.save()
        return HttpResponseRedirect(self.success_url+'&success=1')

class PaquetePublicidadList(ListView):
	model = PaquetePublicidad
	paginate_by = 10

class OrdenList(ListView):
	model = Orden
	paginate_by = 10