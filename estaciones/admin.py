# -*- coding: utf-8 -*-#
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.forms import ModelForm

from django.contrib.flatpages.models import FlatPage
from django.contrib.flatpages.admin import FlatPageAdmin as FlatPageAdminOld

from django.db import models
from estaciones.models import Estacion, FrecuenciaCobertura, Provincia, Cliente, PaquetePublicidad, HorarioRotativo, Publicidad, PreciosCunas
from estaciones.forms import ClienteForm

class FlatPageAdmin(FlatPageAdminOld):
    class Media:
	    js = [
	        '/static/grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
	        '/static/js/tinymce_setup.js',
	    ]

class ParrillaInline(admin.TabularInline):
    model = PaquetePublicidad
    verbose_name_plural = 'Parrilla de Programación'
    

class PreciosInline(admin.TabularInline):
    model = PreciosCunas
    extra = 1
    
class HorarioRotativoInline(admin.TabularInline):
    model = HorarioRotativo
    inlines = [PreciosInline]
    extra = 2
    
class EstacionAdmin(admin.ModelAdmin):
	fieldsets = (("Datos de la Estación de Radio", {
		'fields' : ('nombre', 'descripcion', ('categorias','logo'), 'en_promocion_desde', 'nivel_socioeconomico', 'nivel_edad_target', 'cobertura_frecuencias')
		}), 
	)
	list_filter = ('nivel_socioeconomico','categorias__name', 'en_promocion_desde', 'nivel_edad_target', 'cobertura_frecuencias__provincia__provincia', 'cobertura_frecuencias__provincia__region')
	search_fields = ('nombre',
					'slug',
					'descripcion',
					'nivel_socioeconomico',
					'cobertura_frecuencias__provincia__region'
					)
	save_as = True
	list_per_page = 10
	list_display = ('nombre', 'slug', 'sumario_descripcion','logotipo' )#Falta logo
	list_display_links = ('nombre', 'slug',)
	#raw_id_fields = ['cobertura_frecuencias']
	#related_lookup_fields = {'m2m':['cobertura_frecuencias']}
	filter_horizontal = ('cobertura_frecuencias',)

	inlines = [
        ParrillaInline,
        HorarioRotativoInline,
    ]
	class Media:
	    js = [
	        '/static/grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
	        '/static/js/tinymce_setup.js',
	    ]
	
class ParrillaAdmin(admin.ModelAdmin):
	list_display = ('estacion', 'programa', 'horario', 'emision', 'precio' )
	fields = (('estacion', 'programa'), ('emision', 'horario'), 'precio')
	list_display_links = ('programa',)
	list_filter = ('emision',)
	list_per_page = 10

class FrecuenciaCoberturaAdmin(admin.ModelAdmin):
	list_display = ('frecuencia', 'modulacion', 'provincia')
	search_fields = ('frecuencia', 'modulacion', 'provincia__provincia')
	list_filter = ('provincia__provincia',)
	list_per_page = 10

class ProvinciaAdmin(admin.ModelAdmin):
	exclude = ('provincia',)
	list_display = ('codigo_ec', 'provincia', 'region')
	search_fields = ('codigo_ec', 'provincia', 'region')
	list_per_page = 10

class ClienteEmbebido(admin.StackedInline):
	form = ClienteForm
	model = Cliente
	can_delete = False
	verbose_name_plural = 'clientes'

class UserAdmin(UserAdmin):
    inlines = (ClienteEmbebido, )

class PublicidadAdmin(admin.ModelAdmin):
    """
    Administración de banners y publicidad en el sitio
    """
    list_display = ('show_date', 'hide_date', 'promo_price')
    fields = (('show_date', 'hide_date'), 'promo_price', 'descripcion')
    
    

admin.site.register(Estacion, EstacionAdmin)
admin.site.register(PaquetePublicidad, ParrillaAdmin)
admin.site.register(FrecuenciaCobertura, FrecuenciaCoberturaAdmin)
admin.site.register(Provincia, ProvinciaAdmin)

admin.site.unregister(FlatPage)
admin.site.register(FlatPage, FlatPageAdmin)
admin.site.register(Publicidad, PublicidadAdmin)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
