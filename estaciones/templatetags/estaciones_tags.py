from django import template
from estaciones.views import EstacionList
from django.contrib.contenttypes.models import ContentType
from estaciones.models import PaquetePublicidad, HorarioRotativo
register = template.Library()

@register.simple_tag(takes_context=True)
def get_page_in_details_paginator(context, index, page):
	page_size = EstacionList.paginate_by
	if page == '':
		page = 1
	return "%s" % str(page_size * (int(page)-1) + int(index))


@register.simple_tag(takes_context=True)
def content_type_for_paquete_publicidad(context):
	return ContentType.objects.get_for_model(PaquetePublicidad).pk


@register.simple_tag(takes_context=True)
def content_type_for_horario_rotativo(context):
	return ContentType.objects.get_for_model(HorarioRotativo).pk

