# -*- coding: utf-8 -*-#
from django import forms
from django.forms.widgets import CheckboxSelectMultiple
from orders.models import Orden
from estaciones.models import PaquetePublicidad, HorarioRotativo
from django.contrib.contenttypes.models import ContentType

def get_product_data():
	paquetes = PaquetePublicidad.objects.all()
	horarios_rotativos = HorarioRotativo.objects.all()
	result = []
	for paquete in paquetes:
		result.append(("%s:%s" % (ContentType.objects.get_for_model(PaquetePublicidad).pk, paquete.pk),
					paquete.__unicode__()
					))
	for horario_rot in horarios_rotativos:
		result.append(("%s:%s" % (ContentType.objects.get_for_model(HorarioRotativo).pk, horario_rot.pk),
					horario_rot.__unicode__()
					))
	print tuple(result)
	return tuple(result)

class CartForm(forms.ModelForm):
	product_object = forms.ChoiceField(choices=get_product_data())
	class Meta:
		model = Orden
		fields = ('product_object', 'cantidad', 'observaciones', 'audio')
