from estaciones.models import Estacion, HorarioRotativo, PaquetePublicidad, PreciosCunas
from tastypie import fields
from django.contrib.auth.models import Group
from tastypie.authentication import SessionAuthentication
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS


class EstacionResource(ModelResource):
    class Meta:
        queryset = Estacion.objects.all()
        authentication = SessionAuthentication()

class PaquetePublicidadResource(ModelResource):
	estacion = fields.ForeignKey(EstacionResource, 'estacion')

	class Meta:
		queryset = PaquetePublicidad.objects.all()
		filtering = {'estacion': ALL_WITH_RELATIONS,}
		authentication = SessionAuthentication()

class HorarioRotativoResource(ModelResource):
    estacion = fields.ForeignKey(EstacionResource, 'estacion')
    precio_regional = fields.CharField(attribute='precio_regional', readonly=True)
    
    class Meta:
		queryset = HorarioRotativo.objects.all()
		filtering = {'estacion': ALL_WITH_RELATIONS,}
		authentication = SessionAuthentication()
        
    def dehydrate(self, bundle):
        group = bundle.request.user.groups.all()[0]
        if group:
            pc = PreciosCunas.objects.filter(cuna=bundle.obj.pk, group= group.pk)
        else:
            pc = PreciosCunas.objects.filter(cuna=bundle.obj.pk)
            
        bundle.data['precio_nacional'] = pc[0].precio_nacional
        return bundle
        
        