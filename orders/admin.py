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
import os
import zipfile
from cStringIO import StringIO
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.defaults import patterns

from django.http import HttpResponse
from django.contrib import admin
from django.db.models import get_model
from django.db import models
from orders.models import PaquetePublicidad, Audios, HorariosPautas

from xlsxwriter.workbook import Workbook

Orden = get_model('orders', 'Orden')
#PaquetePublicidad = get_model('orders', 'PaquetePublicidad')


def archivo_plano_orden(request, orden):
    """
    GENERA ARCHIVO XSLX PARA LA ORDEN
    """
    xls = StringIO()
    
    workbook = Workbook(xls)
    worksheet = workbook.add_worksheet()
    
    worksheet.write('A1', 'DATOS A EXPORTAR PARA TRAFFIC')
    worksheet.write('A2', 'anunciaenradios')
    worksheet.write('A4', '')
    worksheet.write('A5', 'DATOS GENERALES')
    
    workbook.close()
    
    # Dar la respuesta
    xls.seek(0)
    
    response = HttpResponse(xls.read(), mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;charset=utf-8")
    response['Content-Disposition'] = "attachment; filename=datos-traffic.xlsx"

    return response

def descargar_audios(request, orden):
    """
    Descargar un zip con los audios de una Orden
    """
    
    filenames = [audio.file.name for audio in Audios.objects.filter(paquete=orden)]
        
    zip_subdir = "audios"
    zip_filename = "%s-Orden-%s.zip" % (zip_subdir, orden)
    
    s = StringIO()
    
    zf = zipfile.ZipFile(s, "w")
    for fpath in filenames:
        fdir, fname = os.path.split(fpath)
        zip_path = os.path.join(zip_subdir, fname)
        
        zf.write('%s/%s' %(settings.MEDIA_ROOT, fpath), zip_path)
    zf.close()
    
    resp = HttpResponse(s.getvalue(), mimetype = "application/x-zip-compressed")
    resp['Content-Disposition'] = 'attachment; filename=%s' % zip_filename
    
    return resp

def get_admin_urls(urls):
    def get_urls():
        my_urls = patterns('',
            url(r'^archivoplano/(?P<orden>[\w-]+)/*$', admin.site.admin_view(archivo_plano_orden), name="excel"),
            url(r'^descargaaudios/(?P<orden>[\d]+)/$', admin.site.admin_view(descargar_audios), name="audio_descarga")
            
        )
        return my_urls + urls
    return get_urls



class HorariosInline(admin.TabularInline):
    model = HorariosPautas
    
class AudiosInline(admin.TabularInline):
    model = Audios


class OrdenAdmin(admin.ModelAdmin):
    """
    Interfaz para administrar órdenes registradas en el sistema
    """    
    raw_id_fields = ['cliente']
    fields = (('numero','fecha_creada'), ('total_incl_iva', 'iva', 'total_gral',), 'cliente', 'cantidad', 'producto', ('paquete_publicidad', 'changeform_link', 'audios_link',), 'archivo_link',)
    list_display = ('numero', 'total_incl_iva', 'cliente', 'fecha_creada', 'cantidad', 'producto', 'paquete_publicidad')
    list_filter = ('fecha_creada', 'cliente__username',)
    readonly_fields = ('paquete_publicidad', 'iva', 'total_gral', 'changeform_link', 'producto', 'fecha_creada', 'archivo_link', 'audios_link',)
    #readonly_fields = ('numero', 'total_incl_iva')


class PaquetePublicidadAdmin(admin.ModelAdmin):
    list_display = ('observaciones', 'duenno')
    list_filter = ('duenno',)
    inlines = [HorariosInline, AudiosInline,]




admin.site.register(Orden, OrdenAdmin)
admin.site.register(PaquetePublicidad, PaquetePublicidadAdmin)

admin_urls = get_admin_urls(admin.site.get_urls())
admin.site.get_urls = admin_urls
