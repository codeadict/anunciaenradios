from django.conf.urls import url, include, patterns
from django.views.generic import TemplateView
from haystack.views import search_view_factory
from haystack.forms import FacetedSearchForm
from estaciones.forms import BuscarEstacionForm
from haystack.query import SearchQuerySet
from haystack.views import SearchView, FacetedSearchView
from estaciones.views import EstacionDetailView, EstacionList, DetallesCarruselEstacionList
from django.contrib.auth.decorators import login_required

from tastypie.api import Api
from estaciones.api import EstacionResource, HorarioRotativoResource, PaquetePublicidadResource

#Registering the API
v1_api = Api(api_name='v1')
v1_api.register(EstacionResource())
v1_api.register(PaquetePublicidadResource())
v1_api.register(HorarioRotativoResource())

urlpatterns = patterns("",
	url(r'^$', EstacionList.as_view(), name='estaciones/lista_estaciones'),
	url(r'^por_pagina/$', DetallesCarruselEstacionList.as_view(template_name='estaciones/estacion_details_carousel.html'),
									name='por_pagina'),
    url(r'^detalles/(?P<slug>[-_\w]+)/$', login_required(EstacionDetailView.as_view(template_name='estaciones/estacion_details.html'),
    													login_url='/administrar'), name="detalles"),        											
    (r'^comentarios/', include('django.contrib.comments.urls')),
    (r'^api/', include(v1_api.urls)),
)

urlpatterns += patterns('haystack.views',
    url(r'^buscar/$', search_view_factory(
        view_class=FacetedSearchView,
        searchqueryset=SearchQuerySet().facet('categorias'),
        form_class=BuscarEstacionForm
    ), name='haystack_search'),
)