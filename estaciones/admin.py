# -*- coding: utf-8 -*-#
from django.contrib import admin
from django.forms import ModelForm
from wysiwyg import ElrteWidget
# from models import Estacion - creo que este esta de más

from django.contrib.flatpages.models import FlatPage
from django.contrib.flatpages.admin import FlatPageAdmin as FlatPageAdminOld

from django.db import models
from estaciones.models import Estacion, NivelSocioEconomico, NivelEdadTarget, \
	FrecuenciaCobertura, Provincia #,User


class FlatPageAdmin(FlatPageAdminOld):
    formfield_overrides = {
        models.TextField: {'widget': ElrteWidget()},
    }

class EstacionAdmin(admin.ModelAdmin):
	formfield_overrides = {
        models.TextField: {'widget': ElrteWidget()},
    }

	fieldsets = (("Datos de las estaciones de radio", {
		'fields' : ('nombre', 'descripcion', 'categorias','logo', 'nivel_socioeconomico')
		}), 
	)
	list_filter = ('nivel_socioeconomico__tipo','categorias__name')
	search_fields = ('nombre',
					'slug',
					'descripcion',
					'nivel_socioeconomico__tipo'
					'en_promocion_desde'
					)
	save_as = True
	list_per_page = 10
	list_display = ('nombre', 'slug', )#Falta logo
	list_display_links = ('nombre', 'slug',)
	raw_id_fields = ['nivel_socioeconomico']
	related_lookup_fields = {'m2m':['nivel_socioeconomico']}
	#filter_horizontal = ('nivel_socioeconomico',)
	#form = EstacionForm

class NivelSocioEconomicoAdmin(admin.ModelAdmin):
	list_display = ('tipo',)
	search_fields = ('tipo',)
	list_per_page = 10

class NivelEdadTargetAdmin(admin.ModelAdmin):
	list_display = ('rango_edad', 'nivel_socioeconomico')
	search_fields = ('rango_edad', 'nivel_socioeconomico__tipo')
	list_filter = ('nivel_socioeconomico__tipo',)
	list_per_page = 10

class FrecuenciaCoberturaAdmin(admin.ModelAdmin):
	list_display = ('frecuencia', 'modulacion', 'provincia' , 'nivel_edad_target')
	search_fields = ('frecuencia', 'modulacion', 'provincia__provincia', 'nivel_edad_target__rango_edad')
	list_filter = ('provincia__provincia', 'nivel_edad_target__rango_edad')
	list_per_page = 10

class ProvinciaAdmin(admin.ModelAdmin):
	list_display = ('codigo', 'provincia', 'region')
	search_fields = ('codigo', 'provincia', 'region')
	list_per_page = 10

admin.site.register(Estacion, EstacionAdmin)
admin.site.register(NivelSocioEconomico, NivelSocioEconomicoAdmin)
admin.site.register(NivelEdadTarget, NivelEdadTargetAdmin)
admin.site.register(FrecuenciaCobertura, FrecuenciaCoberturaAdmin)
admin.site.register(Provincia, ProvinciaAdmin)

admin.site.unregister(FlatPage)
admin.site.register(FlatPage, FlatPageAdmin)