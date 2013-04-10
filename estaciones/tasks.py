from __future__ import absolute_import

from django.core.management import call_command

from django.core.exceptions import ImproperlyConfigured
from django.core.management import call_command
from django.db.models.loading import get_model
from celery.utils.log import get_task_logger
from celery import task
from estaciones.models import Estacion

try:
	from haystack import connections, connection_router
	from haystack.exceptions import NotHandled as IndexNotFoundException
	legacy = False
except ImportError:
	try:
		from haystack import site
		from haystack.exceptions import NotRegistered as IndexNotFoundException # noqa
		legacy = True
	except ImportError, e:
		raise ImproperlyConfigured("Haystack couldn't be imported: %s" % e)

logger = get_task_logger(__name__)

def get_indexes(model_class, **kwargs):
	"""
	Fetch the model's registered ``SearchIndex`` in a standarized way.
	"""
	try:
		if legacy:
			index_holder = site
			yield index_holder.get_index(model_class)
		else:
			using_backends = connection_router.for_write(**{'models': [model_class]})
			for using in using_backends:
				index_holder = connections[using].get_unified_index()
				yield index_holder.get_index(model_class)
	except IndexNotFoundException:
		raise ImproperlyConfigured("Couldn't find a SearchIndex for %s." % model_class)

@task
def update_es_index():
    call_command('update_index')

@task
def update_estaciones_es_index(action, pk, **kwargs):
	try:
		logger.info('Updating estacion id=%s' % pk)
		instance = Estacion.objects.get(pk=pk)

		for current_index in get_indexes(Estacion, **kwargs):
			current_index_name = ".".join([Estacion.__module__, current_index.__class__.__name__])
			if action == 'delete':
				current_index.remove_object(instance)
			elif action == 'update':
				current_index.update_object(instance)
	except Exception, exc:
		logger.error(exc)
		update_estaciones_es_index.retry([action, pk], kwargs, exc=exc)

