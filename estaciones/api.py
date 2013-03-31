from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie import fields
from estaciones.models import Estacion, HorarioRotativo, PaquetePublicidad


class EstacionResource(ModelResource):
    class Meta:
        queryset = Estacion.objects.all()

class PaquetePublicidadResource(ModelResource):
	estacion = fields.ForeignKey(EstacionResource, 'estacion')
	class Meta:
		queryset = PaquetePublicidad.objects.all()
		filtering = {'estacion': ALL_WITH_RELATIONS,}

class HorarioRotativoResource(ModelResource):
	estacion = fields.ForeignKey(EstacionResource, 'estacion')

	class Meta:
		queryset = HorarioRotativo.objects.all()
		filtering = {'estacion': ALL_WITH_RELATIONS,}
