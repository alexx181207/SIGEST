from django import forms

from django.forms import ModelForm

# from django.contrib.auth.models import User
from .models import OrdenPrimaria

# import datetime


class RepairForm(ModelForm):
    class Meta:
        model = OrdenPrimaria
        fields = ["accion_reparacion", "estado", "mano_obra"]

        widgets = {
            "accion_reparacion": forms.TextInput(
                attrs={
                    "class": "form-control col-md-7 col-xs-12 forms-input",
                }
            ),
            "estado": forms.Select(
                attrs={
                    "class": "select2_single form-control forms-input",
                }
            ),
            "mano_obra": forms.Select(
                attrs={"class": "select2_single form-control forms-input"}
            ),
        }








"""class BuscarServicioForm(forms.Form):
    prefijo = forms.CharField()
    fecha_inicio = forms.DateTimeField()
    fecha_fin = forms.DateTimeField()


class BuscarOrdenForm(forms.Form):
    orden = forms.CharField()"""


"""class DefectarModel(forms.ModelForm):
	class Meta:
		model=OrdenReparada
		fields = ['accion_reparacion', 'recursos', 'estado_defectadas']

class EntregarModel(forms.ModelForm):
	class Meta:
		model=OrdenPrimaria
		fields = ['fecha_entrada_taller']"""
