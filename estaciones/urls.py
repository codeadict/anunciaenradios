from django.conf.urls import url, include, patterns
from django.views.generic import TemplateView
from haystack.views import search_view_factory
from haystack.forms import FacetedSearchForm
from estaciones.forms import BuscarEstacionForm
from haystack.query import SearchQuerySet
from haystack.views import SearchView, FacetedSearchView
from estaciones.views import EstacionDetailView

urlpatterns = patterns("",
    url(r'^$',
        TemplateView.as_view(template_name='index.html'),
        name='website_index'),
    url(r'^detalles/(?P<slug>[-_\w]+)/$', EstacionDetailView.as_view(template_name='detalles.html'), name='detalles')
)

urlpatterns += patterns('haystack.views',
    url(r'^buscar/$', search_view_factory(
        view_class=FacetedSearchView,
        searchqueryset=SearchQuerySet().facet('categorias'),
        form_class=BuscarEstacionForm
    ), name='haystack_search'),
)