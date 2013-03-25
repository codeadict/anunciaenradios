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
    logo = models.FileField(upload_to="logos", max_length=1024 * 2, blank=True, null=True, verbose_name="logo", help_text="Máximo 2MB")
    # TODO: categorias con django taggit
    # TODO: en_promocion = models.DateTimeField(null=True, blank=True) ? no está en el word!!!, es necesario?
    nivel_socioeconomico = models.ForeignKey(NivelSocioEconomico, blank=False, null=False, verbose_name="nivel socioeconómico")
    
    class Meta:
        db_table = 'estaciones_radio'
        verbose_name = 'Estación de Radio'
        verbose_name_plural = 'Estaciones de Radio'
        
    def __unicode__(self):
        return u'%s' % (self.slug)
    
    
class NivelSocioEconomico(models.Model):
    nombre = models.CharField(max_length=100, unique=True, null=False, verbose_name="nivel socioeconómico")
    # TODO: a lo mejor nombre (o tipo) se puede definir de la siguiente manera (suponiendo que tiene un número finito pequeño de ocurrencias)
    # por ej:
    # NSE = (
    #         (u'B', u'Bajo'),
    #         (u'M', u'Medio')
    #         (u'A', u'Alto')
    #         )
    # nombre (o tipo) = models.CharField(max_length=1, choices=NSE, verbose_name="nivel socioeconómico")
    
    nivel_edad_target = models.ForeignKey(NivelEdadTarget, blank=False, null=False, verbose_name="rango de edades")
    
    class Meta:
        verbose_name = 'Nivel Socioeconómico'
        verbose_name_plural = 'Niveles Socioeconómicos'
        
    def __unicode__(self):
        return u'%s' % (self.nombre)
    

class NivelEdadTarget(models.Model):
    # TODO: a lo mejor con nombre sucede lo mismo que con el modelo de arriba
    nombre = models.CharField(max_length=50, null=False, verbose_name="rango de edad")
    frecuencia_cobertura = models.ForeignKey(FrecuenciaCobertura, blank=False, null=False, verbose_name="cobertura de frecuencia")

    class Meta:
        verbose_name = 'Rango de edad'
        verbose_name_plural = 'Rangos de edades'
        
    def __unicode__(self):
        return u'%s' % (self.nombre)

class FrecuenciaCobertura(models.Model):
    MODULACION = (
        (u'AM')
        (u'FM')
        )
    frecuencia = models.FloatField()
    modulacion = models.CharField(max_length=2, choices=MODULACION, verbose_name="modulación")
    provincia = models.ForeignKey(Provincia, blank=False, null=False, verbose_name="provincia")

    class Meta:
        verbose_name = 'Cobertura de la Frecuencia'
        verbose_name_plural = 'Coberturas de Frecuencias'
        
    def __unicode__(self):
        return u'%s-%s' % (self.frecuencia, self.modulacion)

class Provincia(models.Model):
    REGION = (
        (u'C', u'Costa')
        (u'S', u'Sierra')
        (u'O', u'Oriente')
        (u'G', u'Galápagos')
        )

    codigo = models.CharField(max_length=50, null=False, verbose_name="código")
    provincia = models.CharField(max_length=100, null=False, verbose_name="provincia")
    region = models.CharField(max_length=1, choices=REGION, verbose_name="región", def)
    
    class Meta:
        verbose_name = 'Provincia'
        verbose_name_plural = 'Provincias'
        
    def __unicode__(self):
        return u'%s' % (self.provincia)

# TODO: Modelo User
