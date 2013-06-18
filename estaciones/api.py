from estaciones.models import Estacion, HorarioRotativo, PaquetePublicidad
from tastypie import fields
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
    precio_nacional = fields.CharField(attribute='_precio_nacional', readonly=True)
    precio_regional = fields.CharField(attribute='_precio_regional', readonly=True)
    
    class Meta:
		queryset = HorarioRotativo.objects.all()
		filtering = {'estacion': ALL_WITH_RELATIONS,}
		authentication = SessionAuthentication()
        
        
