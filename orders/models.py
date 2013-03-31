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

from django.conf import settings
from django.db import models
from django.contrib.auth.models import User


class Orden(models.Model):
    """
    Modelo de una Orden de compra en el sistema
    """
    numero = models.CharField(u'Número de Orden', max_length=128, db_index=True)
    cliente = models.ForeignKey(User, related_name='ordenes', null=True, blank=True, verbose_name="Cliente")    
    total_incl_iva = models.DecimalField("Total orden (inc. IVA)", decimal_places=2, max_digits=12)
    #indica el estado de la Orden
    estado = models.CharField("Estado", max_length=100, null=True, blank=True)
    #fecha de creada la orden
    fecha_creada = models.DateTimeField(auto_now_add=True, db_index=True)
    
    class Meta:
        ordering = ['-fecha_creada',]
        permissions = (
            ("can_view", "Puede ver Órdenes"),
        )
        verbose_name = "Orden"
        verbose_name_plural = "Órdenes"
        
    def __unicode__(self):
        return u"#%s" % (self.numero,)
    
    def v_hash(self):
        return hashlib.md5('%s%s' % (self.number, settings.SECRET_KEY)).hexdigest()
    
    
