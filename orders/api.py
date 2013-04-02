from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie import fields
from orders.models import Orden
from tastypie.authentication import SessionAuthentication
from tastypie.authorization import Authorization, DjangoAuthorization
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType

class UserResource(ModelResource):
	class Meta:
		queryset = User.objects.all()

class ContentTypeResource(ModelResource):
	class Meta:
		queryset = ContentType.objects.all()

class OrdenResource(ModelResource):
	user = fields.ForeignKey(UserResource, 'cliente')
	content_type = fields.ForeignKey(ContentTypeResource, 'content_type')

	class Meta:
		queryset = Orden.objects.all()
		#authentication = SessionAuthentication()
		authorization = DjangoAuthorization() #valorar si es necesario DjangoAuthorization o solo Authorization