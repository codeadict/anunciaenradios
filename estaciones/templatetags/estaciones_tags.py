from django import template
from estaciones.views import EstacionList
register = template.Library()

@register.simple_tag(takes_context=True)
def get_page_in_details_paginator(context, index, page=1):
	page_size = EstacionList.paginate_by
	return "%s" % str(page_size * (int(page)-1) + int(index))