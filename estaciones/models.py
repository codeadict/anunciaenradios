# -*- coding: utf-8 -*-
import logging
from django.template.defaultfilters import slugify
from settings import *
from django.db import models
from taggit.managers import TaggableManager
from django.contrib.auth.models import User
from django_localflavor_ec.ec_provinces import PROVINCE_CHOICES
from registration.supplements import RegistrationSupplementBase

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
    descripcion = models.TextField(verbose_name = "descripción", help_text='breve descripción de la estación de radio')
    logo = models.FileField(upload_to=settings.UPLOAD_DIRECTORY, max_length=1024 * 2, blank=True, null=True, verbose_name="logo de la estación", help_text="Máximo 2MB")
    categorias = TaggableManager(verbose_name="Categorías", help_text='Categorías de la Radio. Ej. Juvenil, Informativa.')
    en_promocion_desde = models.DateTimeField(null=True, blank=True, verbose_name='en promoción desde')
    nivel_socioeconomico = models.CharField(max_length=10, choices=NSE, blank=False, null=False, verbose_name='nivel socioeconómico')
    nivel_edad_target = models.CharField(max_length=10, choices=NET, blank=False, null=False, verbose_name='rango de edad')
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
    
    def sumario_descripcion(self):
        if self.descripcion:
            return self.descripcion[:240] + "..."
        return u"Sin descripción"
    sumario_descripcion.short_description = 'Descripción'
    sumario_descripcion.admin_order_field = 'descripcion'
    sumario_descripcion.allow_tags = True
        
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

    codigo = models.CharField(max_length=50, choices=PROVINCE_CHOICES, null=False, verbose_name='provincia')
    provincia = models.CharField(max_length=100, null=False, verbose_name='nombre de la provincia')
    region = models.CharField(max_length=10, choices=REGION, verbose_name='región')

    def codigo_ec(self):
        return "EC-%s" % self.codigo
        
    codigo_ec.short_description = 'Código de la provincia'
    codigo_ec.admin_order_field = 'codigo'
    codigo_ec.allow_tags = True

    class Meta:
        verbose_name = 'Provincia'
        verbose_name_plural = 'Provincias'
        unique_together = ['codigo', 'region']
        
    def __unicode__(self):
        return u'%s' % (self.provincia)

    
    def save(self, *args, **kwargs):
        for provincia in PROVINCE_CHOICES:
            if provincia[0] == self.codigo:
                self.provincia = provincia[1]
        super(Provincia, self).save(*args, **kwargs)

class PaquetePublicidad(models.Model):
    '''
    Modelo de Datos para Cunas de Anuncios
    '''
    estacion = models.ForeignKey(Estacion, verbose_name=u'Estación')
    programa = models.CharField(u"Programa", max_length=255, blank=False,
        help_text=u"Programa donde Promocionar, Ej. Barrio Latino")
    horario = models.TimeField(u'Horario', blank=False)
    emision = models.CharField(u'Emisión', max_length=255, blank=False, 
                               help_text="Período de Emisión. Ej. Sábados y Domingos")
    precio = models.DecimalField(u'Precio', max_digits=14, decimal_places=6)
    
    class Meta:
        ordering = ('estacion', 'programa')
        verbose_name = 'Parrilla de Programación'
        verbose_name_plural = 'Parrillas de Programación'
        
    def __unicode__(self):
        return u'Paquete de publicidad[programa:%s - horario:%s]' % (self.programa, self.horario)
    
class HorarioRotativo(models.Model):
    '''
    Modelos para cunas en horario rotativo
    '''
    estacion = models.ForeignKey(Estacion, verbose_name=u'Estación', blank=False, null=False)
    tiempo = models.PositiveIntegerField(u'Tiempo de cuña o mención', help_text=u'Tiempo de cuña o mención en segundos')
    precio_nacional = models.DecimalField(u'Precio Nacional', max_digits=14, decimal_places=6, blank=False)
    precio_regional = models.DecimalField(u'Precio Regional', max_digits=14, decimal_places=6, blank=False)
    
    class Meta:
        verbose_name = 'Cuña en horario rotativo'
        verbose_name_plural = 'Cuñas en horario rotativo'
        
    def __unicode__(self):
        return u'Cuña de horario rotativo[estacion: %s - tiempo en segs: %s' % (self.estacion.nombre, self.tiempo)
    
# TODO: Esto es version 1, mejorar usando la nueva manera que define django 1.5
class Cliente(models.Model):
    usuario = models.OneToOneField(User)
    ruc = models.CharField(max_length=10, null=False, unique=True, blank=False, verbose_name='RUC o Cédula de identidad')
    nombre_compannia = models.CharField(max_length=255, null=False, blank=False, verbose_name='nombre de la compañia del cliente')

      
    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'

    def __unicode__(self):
        return u'%s' % (self.usuario.username)



class ClientRegistrationSupplement(RegistrationSupplementBase):

    ruc = models.CharField(max_length=10, null=False, unique=True, blank=False, verbose_name='RUC o Cédula de identidad')
    nombre_compannia = models.CharField("Nombre de la compañía", max_length=100, help_text="Por favor intruduzca el nombre de su compañia")
    

    def __unicode__(self):
        # a summary of this supplement
        return "RUC: %s / Comp: %s" % (self.ruc, self.nombre_compannia)
