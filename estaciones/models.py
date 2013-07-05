# -*- coding: utf-8 -*-
import logging
from django.template.defaultfilters import slugify
from settings import *
from django.db import models
from taggit.managers import TaggableManager
from django.contrib.auth.models import User, Group
from django.contrib.sessions.models import Session
from django_localflavor_ec.ec_provinces import PROVINCE_CHOICES
from registration.supplements import RegistrationSupplementBase
from django.core.urlresolvers import reverse

from django.utils.safestring import mark_safe


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
            logot = '%s%s' % (settings.MEDIA_URL, self.logo)
        else:
            logot = '%s%s' % (settings.STATIC_URL, '/img/radio-default.png')
        
        return mark_safe(logot)
    
    def sumario_descripcion(self):
        if self.descripcion:
            return self.descripcion[:240] + "..."
        return u"Sin descripción"
    sumario_descripcion.short_description = 'Descripción'
    sumario_descripcion.admin_order_field = 'descripcion'
    sumario_descripcion.allow_tags = True
        
    logotipo.allow_tags = True
    
    def save(self, *args, **kwargs):
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
    horario_i = models.TimeField(u'Hora Inicio', blank=False)
    horario_f = models.TimeField(u'Hora Fin', blank=False)
    emision = models.CharField(u'Emisión', max_length=255, blank=False, 
                               help_text="Período de Emisión. Ej. Sábados y Domingos")
    precio = models.DecimalField(u'Precio', max_digits=14, decimal_places=6)
    
    class Meta:
        ordering = ('estacion', 'programa')
        verbose_name = 'Parrilla de Programación'
        verbose_name_plural = 'Parrillas de Programación'
        
    def __unicode__(self):
        return u'Paquete de publicidad [Programa:%s / Horario:%s] Precio: $%s' % (self.programa, self.horario, self.precio)
    
class HorarioRotativo(models.Model):
    '''
    Modelos para cunas en horario rotativo
    '''
    nombre = models.CharField(u"Nombre", max_length=255, blank=False, null=False, help_text=u'Ejemplo: 20 minutos en horario nocturno')
    estacion = models.ForeignKey(Estacion, verbose_name=u'Estación', blank=False, null=False)
    
    @property
    def precio_nacional(self):
        pc = PreciosCunas.objects.filter(cuna=self.pk)
        return pc[0].precio_nacional
    
    @property
    def precio_regional(self):
        pc = PreciosCunas.objects.filter(cuna=self.pk)
        return pc[0].precio_regional
    
    class Meta:
        verbose_name = 'Cuña de programación'
        verbose_name_plural = 'Cuñas de programación'
        
    def __unicode__(self):
        return u'%s (%s)' % (self.nombre, self.estacion.nombre)
    
    def changeform_link(self):
        if self.id:
            changeform_url = reverse(
                'admin:estaciones_horariorotativo_change', args=(self.id,)
            )
            return u'<a href="%s" target="_blank">Ver/Modificar</a>' % changeform_url
        return u''
    changeform_link.allow_tags = True
    changeform_link.short_description = ''   # omit column header
    
class PreciosCunas(models.Model):
    """
    Precios de las cunas de programación
    """
    precio_nacional = models.DecimalField(u'Precio Nacional', max_digits=14, decimal_places=6, blank=False)
    precio_regional = models.DecimalField(u'Precio Regional', max_digits=14, decimal_places=6, blank=False)
    group = models.ForeignKey(Group, null = False, blank = False, related_name="precios", verbose_name=u'Grupo', help_text='Grupo de clientes de esteos precios')
    cuna = models.ForeignKey(HorarioRotativo, verbose_name=u'Cuña', blank=False, null=False)
   
    class Meta:
        verbose_name = 'Precios Cuña de Programación'
        
    def __unicode__(self):
        return u'Precio Grupo: $%s' % (self.group.name) 
    
    
# TODO: Esto es version 1, mejorar usando la nueva manera que define django 1.5
class Cliente(models.Model):
    usuario = models.OneToOneField(User)
    ruc = models.CharField(max_length=13, null=False, unique=True, blank=False, verbose_name='RUC o Cédula de identidad')
    nombre_compannia = models.CharField(max_length=255, null=False, blank=False, verbose_name='nombre de la compañia del cliente')

      
    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'

    def __unicode__(self):
        return u'%s' % (self.usuario.username)



class ClientRegistrationSupplement(RegistrationSupplementBase):
    ruc = models.CharField(max_length=13, null=False, unique=True, blank=False, verbose_name='RUC o Cédula de identidad')
    nombre_compannia = models.CharField("Nombre de la compañía", max_length=100, help_text="Por favor intruduzca el nombre de su compañia")
    
    def __unicode__(self):
        # a summary of this supplement
        return "RUC: %s / Comp: %s" % (self.ruc, self.nombre_compannia)
    
class Publicidad(models.Model):
    """
    Objeto de Publicidd en el sitio
    """
    descripcion = models.TextField("Descripción", help_text="Texto del Anuncio", blank=False)
    promo_price = models.DecimalField("Precio Promocional", max_digits=14, decimal_places=6, blank=False)
    show_date = models.DateTimeField("Mostrar Desde", blank=False, null=False)
    hide_date = models.DateTimeField("Mostrar Hasta", blank=False, null=False)
    img = models.FileField(verbose_name='Imagen', upload_to='banners', help_text="Imagen de 250px de alto x 683px de ancho")
    promo_idate = models.DateTimeField("Promoción Desde", blank=False, null=False)
    promo_edate = models.DateTimeField("Promoción Hasta", blank=False, null=False)
    product = models.ForeignKey(HorarioRotativo, help_text=u'Producto en promoción')
    
    class Meta:
        verbose_name = 'Oferta'
        verbose_name_plural = 'Ofertas'
        
    def imagen(self):
        if self.img:
            logot = '%s%s' % (settings.MEDIA_URL, self.img)
        
        return mark_safe(logot)
    
    
    
