from django import forms

from django.forms import ModelForm
from Taller.models import OrdenPrimaria

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