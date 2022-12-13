from django import forms

from django.forms import ModelForm

# from django.contrib.auth.models import User
from .models import OrdenPrimaria

# import datetime


class PrimaryOrderForm(ModelForm):
    class Meta:
        model = OrdenPrimaria
        fields = [
            "prefijo",
            "servicio",
            "modelo",
            "defecto",
            "serie",
            "nombre_cliente_entrega",
            "direccion_cliente_entrega",
            "ci_cliente_entrega",
            "contacto_telefono",
            "propietario",
            "folio_venta",
            "fecha_venta",
            "garantia",
            "fecha_vencimiento_garantia",
            "observaciones",
        ]
        widgets = {
            "prefijo": forms.Select(
                attrs={
                    "class": "select2_single form-control forms-input",
                }
            ),
            "modelo": forms.Select(
                attrs={
                    "class": "select2_single form-control forms-input",
                }
            ),
            "servicio": forms.TextInput(
                attrs={"class": "form-control col-md-7 col-xs-12 forms-input"}
            ),
            "ci_cliente_entrega": forms.NumberInput(
                attrs={"class": "form-control col-md-7 col-xs-12 forms-input"}
            ),
            "contacto_telefono": forms.NumberInput(
                attrs={"class": "form-control col-md-7 col-xs-12 forms-input"}
            ),
            "defecto": forms.SelectMultiple(
                attrs={
                    "class": "select2_multiple form-control forms-input",
                }
            ),
            "serie": forms.TextInput(
                attrs={
                    "class": "form-control col-md-7 col-xs-12 forms-input",
                }
            ),
            "fecha_vencimiento_garantia": forms.TextInput(
                attrs={
                    "class": "form-control col-md-7 col-xs-12 forms-input",
                }
            ),
            "folio_venta": forms.TextInput(
                attrs={
                    "class": "form-control col-md-7 col-xs-12 forms-input",
                }
            ),
            "fecha_venta": forms.TextInput(
                attrs={
                    "class": "form-control col-md-7 col-xs-12 forms-input",
                }
            ),
            "nombre_cliente_entrega": forms.TextInput(
                attrs={
                    "class": "form-control col-md-7 col-xs-12 forms-input",
                }
            ),
            "direccion_cliente_entrega": forms.TextInput(
                attrs={
                    "class": "form-control col-md-7 col-xs-12 forms-input",
                }
            ),
            "observaciones": forms.Textarea(
                attrs={
                    "class": "resizable_textarea form-control forms-input",
                }
            ),
            "propietario": forms.CheckboxInput(
                attrs={
                    "class": "flat form-control",
                }
            ),
        }

    """def clean_servicio(self):
        servicio = self.cleaned_data.get("servicio")
        if isinstance(servicio, int) == False:
            raise forms.ValidationError("El servicio debe ser un valor numérico")
        return servicio"""


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


class TalkForm(ModelForm):
    class Meta:
        model = OrdenPrimaria
        fields = ["nombre_cliente"]

        widgets = {
            "nombre_cliente": forms.TextInput(
                attrs={
                    "class": "form-control col-md-7 col-xs-12 forms-input",
                }
            )
        }


class CloseOrderForm(ModelForm):
    class Meta:
        model = OrdenPrimaria
        fields = [
            "nombre_cliente_recibe",
            "direccion_cliente_recibe",
            "ci_cliente_recibe",
        ]

        widgets = {
            "nombre_cliente_recibe": forms.TextInput(
                attrs={
                    "class": "form-control col-md-7 col-xs-12 forms-input",
                }
            ),
            "direccion_cliente_recibe": forms.TextInput(
                attrs={
                    "class": "form-control col-md-7 col-xs-12 forms-input",
                }
            ),
            "ci_cliente_recibe": forms.NumberInput(
                attrs={
                    "class": "form-control col-md-7 col-xs-12 forms-input",
                }
            ),
        }


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


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
