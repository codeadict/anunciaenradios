from django.conf.urls import url, include, patterns
from django.contrib.auth.decorators import login_required

from tastypie.api import Api
from orders.api import OrdenResource, UserResource, ContentTypeResource
from orders.views import OrdenList, CartFormView
from django.contrib.auth.decorators import login_required

#Registering the API
v1_api = Api(api_name='v1')
v1_api.register(OrdenResource())
v1_api.register(UserResource())
v1_api.register(ContentTypeResource())


urlpatterns = patterns("",
    (r'^api/', include(v1_api.urls)),
    url(r'^$', login_required(OrdenList.as_view()), name='lista_ordenes'),
    #url(r'^mis_paquetes/$', login_required(PaquetePublicidadList.as_view()), name='lista_ordenes'),
    url(r'^ordenar/$', login_required(CartFormView.as_view(template_name="orders/orden_form.html"), login_url='/registro/login'), name='ordenar'),
    url(r'^ordenar/exito/$', login_required(CartFormView.as_view(template_name="orders/_compra_exito.html"), login_url='/registro/login'), name='compra_exito'),
    url(r'^ordenes-partial/$', login_required(OrdenList.as_view(template_name="orders/_orden_list.html"), login_url='/registro/login'))

)