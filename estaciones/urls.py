from django.conf.urls import url, include, patterns
from django.views.generic import TemplateView

urlpatterns = patterns("",
    url(r'^$',
        TemplateView.as_view(template_name='index.html'),
        name='website_index'),
    ((r'^buscar/$', include('haystack.urls'))),                      
)