# -*- coding: utf-8 -*-
import logging
from django.template.defaultfilters import slugify
from settings import *
from django.db import models
from taggit.managers import TaggableManager
from django.contrib.auth.models import User
from django.contrib.localflavor.ec.forms import ECProvinceSelect

log = logging.getLogger('ar.estaciones')


class Estacion(models.Model):
    """
    Modelo de Datos para Estaciones de radio
    """
    NSE = (
            (u'Bajo', u'Bajo'),
            (u'Medio', u'Medio'),
            (u'Alto', u'Alto')
            )

    nombre = models.CharField(max_length=255, blank=False, null=False)
    slug = models.SlugField(max_length=130, unique=True, null=True)
    logo = models.FileField(upload_to=settings.UPLOAD_DIRECTORY, max_length=1024 * 2, blank=True, null=True, verbose_name='logo de la estación', help_text='Máximo 2MB')
    descripcion = models.TextField(verbose_name = 'descripción', help_text='breve descripción de la estación de radio')    
    categorias = TaggableManager()
    en_promocion_desde = models.DateTimeField(null=True, blank=True, verbose_name='en promoción desde')
    nivel_socioeconomico = models.CharField(max_length=10, choices=NSE, verbose_name='nivel socioeconómico')
    # TODO: Definir si Nivel target edad pudiera ser otro choices
    niveles_edad_target = models.ManyToManyField('NivelEdadTarget', blank=True, null=True, verbose_name='rangos de edades')
    cobertura_frecuencias = models.ManyToManyField('FrecuenciaCobertura', blank=True, null=True, verbose_name='cobertura y frecuencias')
    
    class Meta:
        db_table = 'estaciones_radio'
        verbose_name = 'Estación de Radio'
        verbose_name_plural = 'Estaciones de Radio'
        
    def __unicode__(self):
        return u'%s' % (self.slug)
    
    def save(self, *args, **kwargs):
        #poner el logo por defecto
        if not self.logo:
            self.logo.name = '%s/default_logo.jpg' % settings.UPLOAD_DIRECTORY
        # auto slugify
        self.slug = slugify(self.nombre)
        super(Estacion, self).save(*args, **kwargs)
    

class NivelEdadTarget(models.Model):
    """
    Modelo de Datos para Rangos de edad
    """    
    rango_edad = models.CharField(max_length=50, null=False, verbose_name='rango de edad')

    class Meta:
        verbose_name = 'Rango de edad'
        verbose_name_plural = 'Rangos de edades'
        
    def __unicode__(self):
        return u'%s' % (self.rango_edad)


class FrecuenciaCobertura(models.Model):
    """
    Modelo de Datos para Área de cobertura y frecuencias
    """   
    MODULACION = (
        (u'AM', u'AM'),
        (u'FM', u'FM')
        )
    frecuencia = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='frecuencia de transmisión')
    modulacion = models.CharField(max_length=2, choices=MODULACION, verbose_name='modulación')
    provincia = models.ForeignKey('Provincia', blank=False, null=False, verbose_name='provincia')

    class Meta:
        verbose_name = 'Cobertura y Frecuencia'
        verbose_name_plural = 'Cobertura y Frecuencias'
        
    def __unicode__(self):
        return u'%s/%s-%s' % (self.provincia, self.frecuencia, self.modulacion)


class Provincia(models.Model):
    """
    Modelo de Datos para Provincias
    """    
    REGION = ((u'Costa', u'Costa'),
              (u'Sierra', u'Sierra'),
              (u'Oriente', u'Oriente'),
              (u'Galapagos', u'Galápagos'))

    codigo = models.CharField(max_length=50, null=False, verbose_name='código')
    provincia = models.CharField(max_length=100, null=False, verbose_name='nombre de la provincia')
    region = models.CharField(max_length=10, choices=REGION, verbose_name='región')

    class Meta:
        verbose_name = 'Provincia'
        verbose_name_plural = 'Provincias'
        
    def __unicode__(self):
        return u'%s' % (self.provincia)

    #TODO:
    #def save(self, *args, **kwargs):
        #p = ECProvinceSelect()
        #super(Estacion, self).save(*args, **kwargs) 

# TODO: Esto es version 1, mejorar usando la nueva manera que define django 1.5
class Cliente(models.Model):
    usuario = models.OneToOneField(User)
    ruc = models.CharField(max_length=10, null=False, blank=False, verbose_name='RUC o Cédula de identidad')
    nombre = models.CharField(max_length=255, null=False, blank=False, verbose_name='nombre de la empresa o del cliente')

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'