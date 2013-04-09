# -*- coding: utf-8 -*-#
# Name: Scrapper para obtener datos de Seguro de Autos del SEi.
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
from django.contrib import admin
from django.db.models import get_model
from django.db import models

Orden = get_model('orders', 'Orden')
#PaquetePublicidad = get_model('orders', 'PaquetePublicidad')


class OrdenAdmin(admin.ModelAdmin):
    """
    Interfaz para administrar órdenes registradas en el sistema
    """    
    raw_id_fields = ['cliente']
    list_display = ('numero', 'total_incl_iva', 'cliente', 'fecha_creada', 'cantidad', 'producto', 'paquete_publicidad')
    list_filter = ('fecha_creada',)
    #readonly_fields = ('numero', 'total_incl_iva')


#class PaquetePublicidadAdmin(admin.ModelAdmin):
#	list_display = ('nombre', 'observaciones', 'audio', 'duenno')
#	list_filter = ('duenno',)
#	class Media:
#	    js = [
#	        '/static/grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
#	        '/static/js/tinymce_setup.js',
#	    ]


admin.site.register(Orden, OrdenAdmin)
#admin.site.register(PaquetePublicidad, PaquetePublicidadAdmin)