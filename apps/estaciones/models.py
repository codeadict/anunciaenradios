# -*- coding: utf-8 -*-
import logging

from django.db import models

log = logging.getLogger('ar.estaciones')


class Estacion(models.Model):
    """
    Modelo de Datos para estaciones de Radio
    """
    nombre = models.CharField(max_length=255, null=False)
    slug = models.CharField(max_length=130, unique=True, null=True)
    descripcion = models.TextField(help_text='Breve descripción de la estación de Radio')
    
    en_promocion = models.DateTimeField(null=True, blank=True)
    
    
    class Meta:
        db_table = 'estaciones_radio'
        verbose_name = 'Estacion de Radio'
        verbose_name_plural = 'Estaciones de Radio'
        
    def __unicode__(self):
        return u'%s: %s' % (self.id)
    
    
class Grupo_Social(models.Model):
    pass

class Edades(models.Model):
    pass

class Regiones(models.Model):
    pass
    
    



