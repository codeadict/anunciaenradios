from estaciones.models import Estacion
from haystack import indexes

class EstacionIndex (indexes.SearchIndex, indexes.Indexable):
	text = indexes.CharField(document=True, use_template=True) #SearchIndex requires there be only one field with document=True.
	#facet search fields
	categorias = indexes.MultiValueField(faceted=True)
	regiones = indexes.MultiValueField()
	edad_target = indexes.CharField(model_attr='niveles_edad_target')

	def get_model(self):
		return Estacion
	
	def prepare_categorias(self, obj):
		return [str(category.name) for category in obj.categorias.all()]

	def prepare_regiones(self, obj):
		return [str(cobertura_frecuencia.provincia.region) for cobertura_frecuencia in obj.cobertura_frecuencias.all()]
