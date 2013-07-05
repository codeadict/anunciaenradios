# -*- coding: utf-8 -*-#
from django.views.generic import FormView, TemplateView, DetailView, ListView 
from django.views.generic import CreateView, DeleteView
from django.contrib.formtools.wizard.views import SessionWizardView


from orders.forms import PaquetePublicidadForm, AudiosFormSet, HorariosFormSet
from orders.models import Orden, PaquetePublicidad, Audios, HorariosPautas
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.dateformat import format
import uuid

from django.utils import simplejson
from django.core.urlresolvers import reverse

from django.contrib import messages


class PautarWizard(SessionWizardView):
    def done(self, form_list, **kwargs):
        return render_to_response('done.html', {
            'form_data': [form.cleaned_data for form in form_list],
        })

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
        context = self.get_context_data()
        self.object = form.save(commit=False)
        audios_form = AudiosFormSet(self.request.POST, self.request.FILES, instance=self.object, prefix='audios')
        horarios_form = HorariosFormSet(self.request.POST, self.request.FILES, instance=self.object, prefix='horarios')    
        if audios_form.is_valid() and horarios_form.is_valid():
            self.object.duenno = self.duenno
        
            #Campos del model Orden
            self.object.save()
            
#             cantidad = 0
#             for form in horarios_form:
#                 if not hasattr(form, 'cleaned_data'):
#                     continue
#                 data = form.cleaned_data
#                 cantidad += data.get('cantidad', 0)
#             if cantidad != 100:
#                 raise ValidationError('La cantidad total de pautas debe ser %(total).2f%%. Actualmente : %(cantidad).2f%%' % {'cantidad': cantidad})
                
            horarios_form.save()
            audios_form.save()
            
    
            # Salvar las ordenes multiples:
            for i in range(len(self.cantidades)):
                object_id = self.object_ids[i]
                content_type = self.content_types[i]
                cantidad = self.cantidades[i]
                total = self.totales[i]
                orden = Orden(numero=self.numero,
                                cliente=self.duenno,
                                total_incl_iva= float(total) * float(cantidad),
                                estado=self.estado,
                                object_id=object_id,
                                content_type=content_type,
                                cantidad=cantidad,
                                paquete_publicidad=self.object)
                orden.save()
                messages.success(self.request, "Ha pautado exitosamente en esta estación. Muchas gracias por su compra.")
        return HttpResponseRedirect(self.success_url)

        
    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))
    
    def get_context_data(self, **kwargs):
        context = super(PaquetePublicidadFormView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['audios_formset'] = AudiosFormSet(self.request.POST, self.request.FILES, instance=self.object, prefix='audios')
            context['horarios_formset'] = HorariosFormSet(self.request.POST, self.request.FILES, instance=self.object, prefix='horarios')
            
        else:
            context['audios_formset'] = AudiosFormSet(instance=self.object, prefix='audios')
            context['horarios_formset'] = HorariosFormSet(instance=self.object, prefix='horarios')
        return context

class PaquetePublicidadList(ListView):
	model = PaquetePublicidad
	paginate_by = 10
    

#Vistas para agregar los audios
def response_mimetype(request):
    if "application/json" in request.META['HTTP_ACCEPT']:
        return "application/json"
    else:
        return "text/plain"

class AudioCreateView(CreateView):
    model = Audios

    def form_valid(self, form):
        self.object = form.save()
        f = self.request.FILES.get('file')
        data = [{'name': f.name, 'url': settings.MEDIA_URL + "audios/" + f.name.replace(" ", "_"), 'delete_url': reverse('upload-delete', args=[self.object.id]), 'delete_type': "DELETE"}]
        response = JSONResponse(data, {}, response_mimetype(self.request))
        response['Content-Disposition'] = 'inline; filename=audios.json'
        return response

    def get_context_data(self, **kwargs):
        context = super(AudioCreateView, self).get_context_data(**kwargs)
        context['audios'] = Audios.objects.all()
        return context


class PictureDeleteView(DeleteView):
    model = Audios

    def delete(self, request, *args, **kwargs):
        """
        This does not actually delete the file, only the database record. But
        that is easy to implement.
        """
        self.object = self.get_object()
        self.object.delete()
        if request.is_ajax():
            response = JSONResponse(True, {}, response_mimetype(self.request))
            response['Content-Disposition'] = 'inline; filename=audios.json'
            return response
        else:
            return HttpResponseRedirect('/upload/new')

class JSONResponse(HttpResponse):
    """JSON response class."""
    def __init__(self,obj='',json_opts={},mimetype="application/json",*args,**kwargs):
        content = simplejson.dumps(obj,**json_opts)
        super(JSONResponse,self).__init__(content,mimetype,*args,**kwargs)


class OrdenList(ListView):
	model = Orden
	paginate_by = 10
    
    
class OrdenDetail(DetailView):
    model = Orden
    slug_field = "numero"
    context_object_name='orden'
    template_name="orden_detail.html"
    
    def get_context_data(self, **kwargs):
        context = super(OrdenDetail, self).get_context_data(**kwargs)
        context['audios'] = Audios.objects.filter(paquete=self.object.paquete_publicidad)
        return context
    
def programacion_map(request, orden):
    #: PK de la orden
    orden = int(orden)
    data = {}
    
    horarios =  HorariosPautas.objects.filter(paquete=orden)
    
    for hr in horarios:
        #convertir a unix timestamp
        f = format(hr.fecha, 'U')
        data.update({str(f): int(hr.cantidad)})
    
    return HttpResponse(simplejson.dumps(data), mimetype='application/json')
    