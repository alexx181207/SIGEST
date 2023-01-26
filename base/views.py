from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import View, TemplateView
from django.views.generic import ListView
from Taller.models import OrdenPrimaria
import datetime

def CalcularTiempo(fecha):
    fechaActual = datetime.datetime.now()
    fechaActual = datetime.datetime.strftime(fechaActual, "%d/%m/%Y")
    fechaActual = datetime.datetime.strptime(fechaActual, "%d/%m/%Y")
    fecha = datetime.datetime.strftime(fecha, "%d/%m/%Y")
    fecha = datetime.datetime.strptime(fecha, "%d/%m/%Y")
    dias = (fechaActual - fecha) / datetime.timedelta(days=1)
    dias += 1
    return int(dias)


class BaseDatosMixin(LoginRequiredMixin, View):
    orden = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        modelComercial = OrdenPrimaria.objects.filter(
            centro=self.request.user.trabajador.centro
        ).filter(confComercial=False)
        cantidad = modelComercial.count()
        modelTaller = (
            OrdenPrimaria.objects.filter(centro=self.request.user.trabajador.centro)
            .filter(confComercial=True)
            .filter(confTaller=False)
        )
        cantidad1 = modelTaller.count()
        context["cantidad"] = cantidad
        context["modelComercial"] = modelComercial
        context["cantidad1"] = cantidad1
        context["modelTaller"] = modelTaller
        return context


class ListMixin(BaseDatosMixin, ListView):
    model = OrdenPrimaria
    module = None

    def __init__(self):
        self.template_name = self.get_template()

    def get_template(self):
        self.template_name = (
            self.module + "/" + self.__class__.__name__.lower() + ".html"
        )
        return self.template_name

    def get_list(self):
        return OrdenPrimaria.objects.filter(centro=self.request.user.trabajador.centro)
