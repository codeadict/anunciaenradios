# -*- coding: utf-8 -*-
import logging
from django.template.defaultfilters import slugify
from settings import *
from django.db import models
from taggit.managers import TaggableManager
from django.contrib.auth.models import User
from django_localflavor_ec.forms import ECProvinceSelect

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

    NET = (
        (u'10-20', u'10-20'),
        (u'21-30', u'21-30'),
        (u'31-40', u'31-40'),
        (u'41-50', u'41-50'),
        (u'51-60', u'51-60'),
        (u'>60', u'>60')
        )

    nombre = models.CharField(max_length=255, blank=False, null=False)
    slug = models.SlugField(max_length=130, unique=True, null=True)
    descripcion = models.TextField(verbose_name = "descripción", help_text='Breve descripción de la estación de Radio')
    logo = models.FileField(upload_to=settings.UPLOAD_DIRECTORY, max_length=1024 * 2, blank=True, null=True, verbose_name="logo de la estación", help_text="Máximo 2MB")
    categorias = TaggableManager(verbose_name="Categorías", help_text='Categorías de la Radio. Ej. Juvenil, Informativa.')
    logo = models.FileField(upload_to=settings.UPLOAD_DIRECTORY, max_length=1024 * 2, blank=True, null=True, verbose_name='logo de la estación', help_text='Máximo 2MB')
    descripcion = models.TextField(verbose_name = 'descripción', help_text='breve descripción de la estación de radio')    
    categorias = TaggableManager()
    en_promocion_desde = models.DateTimeField(null=True, blank=True, verbose_name='en promoción desde')
    nivel_socioeconomico = models.CharField(max_length=10, choices=NSE, blank=False, null=False, verbose_name='nivel socioeconómico')
    # TODO: Definir si Nivel target edad pudiera ser otro choices
    niveles_edad_target = models.CharField(max_length=10, choices=NET, blank=False, null=False, verbose_name='rangos de edades')
    cobertura_frecuencias = models.ManyToManyField('FrecuenciaCobertura', blank=False, null=False, verbose_name='cobertura y frecuencias')
    
    class Meta:
        db_table = 'estaciones_radio'
        verbose_name = 'Estación de Radio'
        verbose_name_plural = 'Estaciones de Radio'
        
    def __unicode__(self):
        return u'%s' % (self.slug)
    
    def logotipo(self):
        if self.logo:
            return u'<img src="/media/%s" width="80" heigth="80" />' % self.logo
        else:
            return u'(Sin imagen)'
        
    logotipo.allow_tags = True
    
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

class PaquetePublicidad(models.Model):
    '''
    Modelo de Datos para Cunas de Anuncios
    '''
    estacion = models.ForeignKey(Estacion, verbose_name=u'Estación')
    programa = models.CharField(u"Programa", max_length=255, blank=False,
        help_text=u"Programa donde Promocionar, Ej. Barrio Latino")
    horario = models.CharField(u'Horario', max_length=255, blank=False)
    emision = models.CharField(u'Emisión', max_length=255, blank=False, 
                               help_text="Período de Emisión. Ej. Sábados y Domingos")
    precio = models.DecimalField(u'Precio', max_digits=14, decimal_places=6)
    
    class Meta:
        ordering = ('estacion', 'programa')
        verbose_name = 'Parrilla de Programación'
        
    def __unicode__(self):
        return u'%s - %s' % (self.programa, self.horario)
    
class HorarioRotativo(models.Model):
    '''
    Modelos para cunas en horario rotativo
    '''
    estacion = models.ForeignKey(Estacion, verbose_name=u'Estación')
    tiempo = models.IntegerField(u'Tiempo de cuña o mención', help_text=u'Tiempo de cuña o mención en segundos')
    precio_nacional = models.DecimalField(u'Precio Nacional', max_digits=14, decimal_places=6)
    precio_regional = models.DecimalField(u'Precio Regional', max_digits=14, decimal_places=6)
    
    class Meta:
        verbose_name = 'Cuña en horario rotativo'
        verbose_name_plural = 'Cuñas en horario rotativo'
        
    def __unicode__(self):
        return u'%s' % (self.estacion.nombre)
    
# TODO: Esto es version 1, mejorar usando la nueva manera que define django 1.5
class Cliente(models.Model):
    usuario = models.OneToOneField(User)
    ruc = models.CharField(max_length=10, null=False, blank=False, verbose_name='RUC o Cédula de identidad')
    nombre = models.CharField(max_length=255, null=False, blank=False, verbose_name='nombre de la empresa o del cliente')

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
