# -*- coding: utf-8 -*-#
# Name: AnunciaenRadios.com
#
# Copyright (C) 2013 DaGaNeT Open Source Solutions
# author: Dairon Medina C. <dairon@daganet.net>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see
# http://www.gnu.org/licenses/agpl-3.0.html.
from decimal import Decimal as D
import hashlib
import datetime
from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.core.urlresolvers import reverse

from django.template.loader import render_to_string
from django.core.mail import send_mail
#added apps
from json_field import JSONField

POSICIONES_TANDA = (('1', 'Normal',), ('2', 'Cabeza de Tanda',), ('2', 'Pie de Tanda',))

CHOICES = (('1', 'Rotativo(Automático)',), ('2', 'Rotativo en Hora Abierta',), ('2', 'Hora Fija',))

class PaquetePublicidad(models.Model):
    observaciones = models.TextField(verbose_name = "observaciones", help_text="Si va a hacer menciones debe poner el texto en este campo.")
    campana = models.CharField(max_length=200, null=True, verbose_name=u"Campaña")
    duenno = models.ForeignKey(User, null=False, blank=False, verbose_name="Dueño")
    
    pautar_en = models.CharField(max_length=1, null=False, default='1', choices=CHOICES, verbose_name="Pautar en")
    hora_inicial = models.TimeField(verbose_name="Hora Inicio", auto_now_add=True, blank=True, null=True)
    hora_fin = models.TimeField(verbose_name="Hora Fin", auto_now_add=True, blank=True, null=True)
        

    class Meta:        
        verbose_name = "Paquete de publicidad"
        verbose_name_plural = "Paquetes de publicidad"
        
    def __unicode__(self):
        return u"#%s: %s" % (self.pk, self.observaciones[:80])
    
    @property
    def es_semanal(self):
        """
        Retorna si es Semanaal o Mensual la Pauta completa
        """
        max_date = HorariosPautas.objects.filter(paquete.pk).aggregate(Max('fecha'))['fecha__max']
        min_date = HorariosPautas.objects.filter(paquete.pk).aggregate(Min('fecha'))['fecha__min']
        
        diff = max_date - min_date
        
        if diff > 7:
            return False
        else:
            return True
            
    
    
class Audios(models.Model):
    file = models.FileField(upload_to="audios", max_length=1024 * 200, blank=False, null=False, verbose_name="Audio")
    slug = models.SlugField(max_length=50, blank=True)
    paquete = models.ForeignKey(PaquetePublicidad, related_name='audios', null=False, blank=False, verbose_name="Paquete de publicidad") 

    def __unicode__(self):
        return self.file.name

    @models.permalink
    def get_absolute_url(self):
        return ('upload-new', )

    def save(self, *args, **kwargs):
        self.slug = self.file.name
        super(Audios, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.file.delete(False)
        super(Audios, self).delete(*args, **kwargs)
        
class HorariosPautas(models.Model):
    """
    Tabla de programacion
    """
    fecha = models.DateField(null=False, blank=False, db_index=True, verbose_name="Fecha")
    cantidad = models.PositiveIntegerField(verbose_name="Cantidad de Cuñas")
    paquete = models.ForeignKey(PaquetePublicidad, related_name='fechas_aire', null=False, blank=False, verbose_name="Paquete de publicidad")
    
    class Meta:
        ordering = ['-fecha',]
        verbose_name = "Fecha Al Aire"
        verbose_name_plural = "Fechas Al Aire"


class Orden(models.Model):
    """
    Modelo de una Orden de compra en el sistema
    """
    ESTADO_ORDEN = (
        (u'Pendiente', u'Pendiente'),
        (u'En proceso', u'En proceso'),
        (u'Aceptada', u'Aceptada'),
        (u'Cancelada', u'Cancelada'),
        (u'Error', u'Error'),
        )
    numero = models.CharField(u'Número de Orden', max_length=128, db_index=True)
    cliente = models.ForeignKey(User, related_name='ordenes', null=False, blank=False, verbose_name="Cliente")    
    total_incl_iva = models.DecimalField("Subtotal", decimal_places=2, max_digits=12)
    #indica el estado de la Orden
    estado = models.CharField("Estado", choices=ESTADO_ORDEN, max_length=100, null=False, blank=False)
    #fecha de creada la orden
    fecha_creada = models.DateTimeField(auto_now_add=True, db_index=True)
    cantidad = models.PositiveIntegerField()
    content_type = models.ForeignKey(ContentType, verbose_name="Tipo de producto")
    object_id = models.PositiveIntegerField(verbose_name="Id")
    producto = generic.GenericForeignKey('content_type', 'object_id')
    paquete_publicidad = models.ForeignKey(PaquetePublicidad, blank=False, null=False)

    class Meta:
        ordering = ['-fecha_creada',]
        permissions = (
            ("can_view", "Puede ver Órdenes"),
        )
        verbose_name = "Orden"
        verbose_name_plural = "Órdenes"
        
    def __unicode__(self):
        return u"#%s" % (self.numero,)
    
    @models.permalink
    def get_absolute_url(self):
        return ('detalle_orden', (), {'numero':self.numero})
    
    def iva(self):
        return self.total_incl_iva * 12/100
    iva.allow_tags = True
    iva.short_description = 'Valor IVA'
    
    def total_gral(self):
        return self.total_incl_iva + self.total_incl_iva * 12/100
    total_gral.short_description = 'Total'
    
    def archivo_link(self):
        return u'<a href="/administrar/archivoplano/%s/" target="_blank">Archivo de la Orden</a>' % self.numero
    archivo_link.allow_tags = True
    archivo_link.short_description = ''
    
    def audios_link(self):
        return u'<a href="/administrar/descargaaudios/%d/" target="_blank">Descargar Audios</a>' % self.pk
    audios_link.allow_tags = True
    audios_link.short_description = ''
    
    def v_hash(self):
        return hashlib.md5('%s%s' % (self.number, settings.SECRET_KEY)).hexdigest()
    
    def changeform_link(self):
        if self.paquete_publicidad:
            changeform_url = reverse(
                'admin:orders_paquetepublicidad_change', args=(self.paquete_publicidad.id,)
            )
            return u'<a href="%s" target="_blank">Ver Datos Cuña</a>' % changeform_url
        return u''
    changeform_link.allow_tags = True
    changeform_link.short_description = ''
    

def send_notification(sender, **kwargs):
    """
    Enviar correo con la orden registrada
    """
    if kwargs['created']:
        obj = kwargs['instance']
        
        subject = 'Orden Registrada en Anunciaenradios'
        
        context = {
               'usuario': obj.cliente,
               'order': obj.pk, 
        }
        message = render_to_string('orders/mail.txt', context)
        try:
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [settings.DEFAULT_FROM_EMAIL])
        except:
            pass

post_save.connect(send_notification, sender=Orden)
