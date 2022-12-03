from django import forms
#from django.forms import ModelForm
#from django.contrib.auth.models import User

#import datetime


class LoginForm(forms.Form):
	username = forms.CharField()
	password = forms.CharField(widget=forms.PasswordInput)

class BuscarServicioForm(forms.Form):
	servicio= forms.CharField()
	fecha_inicio= forms.DateTimeField()
	fecha_fin= forms.DateTimeField()

class BuscarOrdenForm(forms.Form):
	orden= forms.CharField()

"""class DefectarModel(forms.ModelForm):
	class Meta:
		model=OrdenReparada
		fields = ['accion_reparacion', 'recursos', 'estado_defectadas']

class EntregarModel(forms.ModelForm):
	class Meta:
		model=OrdenPrimaria
		fields = ['fecha_entrada_taller']"""






