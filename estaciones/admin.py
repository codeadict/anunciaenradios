# -*- coding: utf-8 -*-#
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.forms import ModelForm
from wysiwyg import ElrteWidget

from django.contrib.flatpages.models import FlatPage
from django.contrib.flatpages.admin import FlatPageAdmin as FlatPageAdminOld

from django.db import models
<<<<<<< HEAD
from estaciones.models import Estacion, NivelSocioEconomico, NivelEdadTarget, \
	FrecuenciaCobertura, Provincia, PaquetePublicidad, HorarioRotativo
=======
from estaciones.models import Estacion, NivelEdadTarget, \
	FrecuenciaCobertura, Provincia, Cliente
>>>>>>> develop


class FlatPageAdmin(FlatPageAdminOld):
    formfield_overrides = {
        models.TextField: {'widget': ElrteWidget()},
    }

class ParrillaInline(admin.TabularInline):
    model = PaquetePublicidad
    verbose_name_plural = 'Parrilla de Programación'
    
class HorarioRotativoInline(admin.TabularInline):
	model = HorarioRotativo
    
class EstacionAdmin(admin.ModelAdmin):
<<<<<<< HEAD
	fieldsets = (("Datos de la Estación de Radio", {
		'fields' : ('nombre', 'descripcion', ('categorias','logo'), 'nivel_socioeconomico')
=======
	formfield_overrides = {
        models.TextField: {'widget': ElrteWidget()},
    }

	fieldsets = (("Datos de las estaciones de radio", {
		'fields' : ('nombre', 'descripcion', 'logo', 'categorias', 'en_promocion_desde', 'nivel_socioeconomico', 'niveles_edad_target', 'cobertura_frecuencias')
>>>>>>> develop
		}), 
	)
	list_filter = ('nivel_socioeconomico','categorias__name', 'en_promocion_desde', 'niveles_edad_target__rango_edad', 'cobertura_frecuencias__provincia__provincia', 'cobertura_frecuencias__provincia__region')
	search_fields = ('nombre',
					'slug',
					'descripcion',
					'nivel_socioeconomico',
					'cobertura_frecuencias__provincia__region'
					)
	save_as = True
	list_per_page = 10
<<<<<<< HEAD
	list_display = ('nombre', 'slug', 'logotipo' )#Falta logo
	list_display_links = ('nombre', 'slug',)
	raw_id_fields = ['nivel_socioeconomico']
	related_lookup_fields = {'m2m':['nivel_socioeconomico']}
	#filter_horizontal = ('nivel_socioeconomico',)
	#form = EstacionForm
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

class NivelSocioEconomicoAdmin(admin.ModelAdmin):
	list_display = ('tipo',)
	search_fields = ('tipo',)
	list_per_page = 10
=======
	list_display = ('nombre', 'slug', 'en_promocion_desde')#Falta logo
	list_display_links = ('nombre', 'slug',)
	raw_id_fields = ['niveles_edad_target', 'cobertura_frecuencias']
	related_lookup_fields = {'m2m':['niveles_edad_target', 'cobertura_frecuencias']}
	
>>>>>>> develop

#TODO: Candidato a desaparecer
class NivelEdadTargetAdmin(admin.ModelAdmin):
	list_display = ('rango_edad',)
	search_fields = ('rango_edad',)
	list_per_page = 10

class FrecuenciaCoberturaAdmin(admin.ModelAdmin):
	list_display = ('frecuencia', 'modulacion', 'provincia')
	search_fields = ('frecuencia', 'modulacion', 'provincia__provincia')
	list_filter = ('provincia__provincia',)
	list_per_page = 10

class ProvinciaAdmin(admin.ModelAdmin):
	list_display = ('codigo', 'provincia', 'region')
	search_fields = ('codigo', 'provincia', 'region')
	list_per_page = 10

class ClienteEmbebido(admin.StackedInline):
    model = Cliente
    can_delete = False
    verbose_name_plural = 'clientes'

# Define a new User admin
class UserAdmin(UserAdmin):
    inlines = (ClienteEmbebido, )

admin.site.register(Estacion, EstacionAdmin)
<<<<<<< HEAD
admin.site.register(PaquetePublicidad, ParrillaAdmin)
admin.site.register(NivelSocioEconomico, NivelSocioEconomicoAdmin)
=======
>>>>>>> develop
admin.site.register(NivelEdadTarget, NivelEdadTargetAdmin)
admin.site.register(FrecuenciaCobertura, FrecuenciaCoberturaAdmin)
admin.site.register(Provincia, ProvinciaAdmin)

admin.site.unregister(FlatPage)
admin.site.register(FlatPage, FlatPageAdmin)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
