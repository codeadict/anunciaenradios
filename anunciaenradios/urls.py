from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from estaciones.views import ContactView

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'anunciaenradios.views.home', name='home'),
    url(r'^$', include('estaciones.urls')),
    url(r'^radios/$',
        TemplateView.as_view(template_name='buscar.html'),
        name='estaciones'),
    url(r'^contacto/$',
        ContactView.as_view(template_name='contacto.html'),
        name='contacto'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^administrar/', include(admin.site.urls)),
    url(r'^grappelli/', include('grappelli.urls')),
)

#urlpatterns += patterns('django.contrib.flatpages.views',
#    (r'^(?P<url>.*)$', 'flatpage'),
#)
