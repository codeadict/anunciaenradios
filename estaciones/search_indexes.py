from estaciones.models import Estacion
from haystack import indexes

class EstacionIndex (indexes.SearchIndex, indexes.Indexable):
	text = indexes.CharField(document=True, use_template=True) #SearchIndex requires there be only one field with document=True.
	#facet search fields
	categorias = indexes.MultiValueField()
	provincia = indexes.MultiValueField()
	edad_target = indexes.MultiValueField()

	def get_model(self):
		return Estacion
	
	def prepare_categorias(self, obj):
		return [category.pk for category in obj.categorias.all()]

	def prepare_provincia(self, obj):
		return [cobertura_frecuencia.provincia.pk for cobertura_frecuencia in obj.cobertura_frecuencias.all()]

	def prepare_edad_target(self, obj):
		return [edad_target.pk for edad_target in obj.niveles_edad_target.all()]		
