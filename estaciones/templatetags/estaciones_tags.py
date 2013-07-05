from datetime import date
from django import template
from estaciones.views import EstacionList
from django.contrib.contenttypes.models import ContentType
from estaciones.models import PaquetePublicidad, HorarioRotativo, Publicidad, Estacion
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

@register.simple_tag(takes_context=True)
def banner_slider(context, tpl='banner.html'):
	"""
	Templatetag para mostrar publicidad
	"""
	try:
		today = date.today()
		banners = Publicidad.objects.filter(show_date__lte=today, hide_date__gte=today)
	except:
		banners = False
		
	t = template.loader.get_template(tpl)
	return t.render(template.Context({'banners': banners}))

@register.simple_tag(takes_context=True)
def home_carousel(context, tpl='carousel.html'):
	"""
	Templatetag para mostrar carrusel con logos en el home
	"""
	try:
		logos = Estacion.objects.all()
	except:
		logos = False
		
	t = template.loader.get_template(tpl)
	return t.render(template.Context({'logos': logos}))

def callMethod(obj, methodName):
	method = getattr(obj, methodName)
	if obj.__dict__.has_key("__callArg"):
		ret = method(*obj.__callArg)
		del obj.__callArg
		return ret
	return method()
 
def args(obj, arg):
	if not obj.__dict__.has_key("__callArg"):
		obj.__callArg = []
	obj.__callArg += [arg]
	return obj
 
register.filter("call", callMethod)
register.filter("args", args)