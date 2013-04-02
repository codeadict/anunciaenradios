from django.conf.urls import url, include, patterns
from django.contrib.auth.decorators import login_required

from tastypie.api import Api
from orders.api import OrdenResource, UserResource, ContentTypeResource

#Registering the API
v1_api = Api(api_name='v1')
v1_api.register(OrdenResource())
v1_api.register(UserResource())
v1_api.register(ContentTypeResource())

urlpatterns = patterns("",
    (r'^api/', include(v1_api.urls)),
)