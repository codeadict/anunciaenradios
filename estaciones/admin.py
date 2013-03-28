# -*- coding: utf-8 -*-#
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.forms import ModelForm
from wysiwyg import ElrteWidget

from django.contrib.flatpages.models import FlatPage
from django.contrib.flatpages.admin import FlatPageAdmin as FlatPageAdminOld

from django.db import models
from estaciones.models import Estacion, FrecuenciaCobertura, Provincia, Cliente


class FlatPageAdmin(FlatPageAdminOld):
    formfield_overrides = {
        models.TextField: {'widget': ElrteWidget()},
    }

class EstacionAdmin(admin.ModelAdmin):
	formfield_overrides = {
        models.TextField: {'widget': ElrteWidget()},
    }

	fieldsets = (("Datos de las estaciones de radio", {
		'fields' : ('nombre', 'descripcion', 'logo', 'categorias', 'en_promocion_desde', 'nivel_socioeconomico', 'niveles_edad_target', 'cobertura_frecuencias')
		}), 
	)
	list_filter = ('nivel_socioeconomico','categorias__name', 'en_promocion_desde', 'niveles_edad_target', 'cobertura_frecuencias__provincia__provincia', 'cobertura_frecuencias__provincia__region')
	search_fields = ('nombre',
					'slug',
					'descripcion',
					'nivel_socioeconomico',
					'cobertura_frecuencias__provincia__region'
					)
	save_as = True
	list_per_page = 10
	list_display = ('nombre', 'slug', 'en_promocion_desde')#Falta logo
	list_display_links = ('nombre', 'slug',)
	raw_id_fields = ['cobertura_frecuencias']
	related_lookup_fields = {'m2m':['cobertura_frecuencias']}
	

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
admin.site.register(FrecuenciaCobertura, FrecuenciaCoberturaAdmin)
admin.site.register(Provincia, ProvinciaAdmin)

admin.site.unregister(FlatPage)
admin.site.register(FlatPage, FlatPageAdmin)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)