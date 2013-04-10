from haystack import signals
from haystack.signals import BaseSignalProcessor
from haystack.exceptions import NotHandled
from django.db import models
from django.db.models.loading import get_model
from estaciones.tasks import update_estaciones_es_index
from estaciones.models import Estacion

class QueuedSignalProcessor(signals.BaseSignalProcessor):
    # Override the built-in.
    def setup(self):
        models.signals.post_save.connect(self.enqueue_save, sender=Estacion)
        models.signals.post_delete.connect(self.enqueue_delete, sender=Estacion)

    # Override the built-in.
    def teardown(self):
        models.signals.post_save.disconnect(self.enqueue_save)
        models.signals.post_delete.disconnect(self.enqueue_delete)

    def enqueue_save(self, sender, instance, **kwargs):
        return update_estaciones_es_index.delay('update', instance.pk)

    def enqueue_delete(self, sender, instance, **kwargs):
        return update_estaciones_es_index.delay('delete', instance.pk)

    def enqueue(self, action, instance, sender, **kwargs):
        """
        Given an individual model instance, determine if a backend
        handles the model, check if the index is Celery-enabled and
        enqueue task.
        """
        using_backends = self.connection_router.for_write(instance=instance)

        for using in using_backends:
            try:
                connection = self.connections[using]
                index = connection.get_unified_index().get_index(sender)
            except NotHandled:
                continue # Check next backend

            
            if action == 'update' and not index.should_update(instance):
                continue
            enqueue_task(action, instance)
            return # Only enqueue instance once