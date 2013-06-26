from django.conf.urls import url, include, patterns
from django.contrib.auth.decorators import login_required

from tastypie.api import Api
from orders.api import OrdenResource, UserResource, ContentTypeResource, PaquetePublicidadResource
from orders.views import PaquetePublicidadFormView, OrdenList, OrdenDetail, PaquetePublicidadList
from django.contrib.auth.decorators import login_required

#Registering the API
v1_api = Api(api_name='v1')
v1_api.register(OrdenResource())
v1_api.register(UserResource())
v1_api.register(ContentTypeResource())
v1_api.register(PaquetePublicidadResource())

urlpatterns = patterns("",
    (r'^api/', include(v1_api.urls)),
    url(r'^$', login_required(OrdenList.as_view()), name='lista_ordenes'),
    url(r'^(?P<slug>[\w-]+)/*$', OrdenDetail.as_view(), name="detalle_orden"),
    url(r'^ajax/programacion/(?P<orden>[\d]+)/$', 'orders.views.programacion_map', name='programacion'),
    url(r'^paquetes/agregar/$', login_required(PaquetePublicidadFormView.as_view(template_name="orders/paquetepublicidad_form.html")), name='agregar_paquete_publicitario')
)