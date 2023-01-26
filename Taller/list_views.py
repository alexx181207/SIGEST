from Comercial.models import OrdenPrimaria
from base.models import Estado, Tecnologia
from base.views import BaseDatosMixin, CalcularTiempo, ListMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
import datetime


class ListadoOrdenesMixin(ListMixin):
    module = "Information"

    def get_queryset(self):
        self.queryset = self.get_list()
        return self.queryset


class ListUpdates(ListadoOrdenesMixin):
    module = "Comercial"

    def get_queryset(self):
        self.queryset = self.get_list().exclude(confComercial=True)
        return self.queryset


class RegistroTFA(ListadoOrdenesMixin):
    module = "Taller"

    def get_queryset(self):
        self.queryset = (
            self.get_list()
            .filter(tecnologia=get_object_or_404(Tecnologia, pk=1))
            .exclude(fecha_entrada_taller=None)
        )
        return self.queryset


class RegistroTB(ListadoOrdenesMixin):
    module = "Taller"

    def get_queryset(self):
        self.queryset = (
            self.get_list()
            .filter(tecnologia=get_object_or_404(Tecnologia, pk=2))
            .exclude(fecha_entrada_taller=None)
        )
        return self.queryset


class ListadoPendientes(ListadoOrdenesMixin):
    module = "Taller"

    def get_queryset(self):
        self.queryset = (
            self.get_list()
            .exclude(fecha_entrada_taller=None)
            .exclude(estado=get_object_or_404(Estado, pk=3))
            .exclude(estado=get_object_or_404(Estado, pk=4))
        )
        return self.queryset


class ListadoReparadas(ListadoPendientes):
    def get_queryset(self):
        self.queryset = (
            self.get_list()
            .exclude(cerrada=True)
            .exclude(estado=get_object_or_404(Estado, pk=1))
            .exclude(estado=get_object_or_404(Estado, pk=2))
        )
        return self.queryset


class GestionTelefono(ListadoOrdenesMixin):
    module = "Comercial"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        model1 = (
            OrdenPrimaria.objects.filter(centro=self.request.user.trabajador.centro)
            .exclude(cerrada=True)
            .exclude(estado=get_object_or_404(Estado, pk=1))
            .exclude(estado=get_object_or_404(Estado, pk=2))
            .filter(nombre_cliente=None)
        )
        model2 = (
            OrdenPrimaria.objects.filter(centro=self.request.user.trabajador.centro)
            .exclude(cerrada=True)
            .exclude(estado=get_object_or_404(Estado, pk=1))
            .exclude(estado=get_object_or_404(Estado, pk=2))
            .exclude(nombre_cliente=None)
            .filter(impresion=False)
            .filter(llama=self.request.user.trabajador)
        )
        context["model1"] = model1
        context["model2"] = model2
        return context


class EntregarOrdenesTaller(ListadoOrdenesMixin):
    module = "Miscelaneos"

    def get_queryset(self):
        self.queryset = self.get_list().filter(confComercial=False)
        return self.queryset


class ConfirmarOrdenesTaller(EntregarOrdenesTaller):
    def get_queryset(self):
        self.queryset = (
            self.get_list().filter(confComercial=True).filter(confTaller=False)
        )
        return self.queryset


"""class EntregaOrdenTaller(ListadoOrdenesMixin):
    module="Miscelaneos"

    def get_queryset(self, ordenprimaria_id):
        self.queryset = self.get_list().filter(confComercial=False)
        self.queryset=get_object_or_404(self.queryset, id=ordenprimaria_id)
        return self.queryset

    def get(self, request, ordenprimaria_id):
        modelo=self.get_list().filter(confComercial=False)
        modelo=get_object_or_404(modelo, id=ordenprimaria_id)
        return modelo"""


@login_required
def EntregaOrdenTaller(request, ordenprimaria_id):
    Orden = OrdenPrimaria.objects.filter(centro=request.user.trabajador.centro)
    modelComercial = Orden.filter(confComercial=False)
    cantidad = modelComercial.count()
    modelTaller = Orden.filter(confComercial=True).filter(confTaller=False)
    cantidad1 = modelTaller.count()
    # model=OrdenPrimaria.objects.filter(centro=request.user.trabajador.centro).filter(fecha_entrada_taller=None).filter(id=ordenprimaria_id)
    model = get_object_or_404(OrdenPrimaria, id=ordenprimaria_id)
    return render(
        request,
        "Miscelaneos/entregaordentaller.html",
        {
            "cantidad": cantidad,
            "modelComercial": modelComercial,
            "cantidad1": cantidad1,
            "modelTaller": modelTaller,
            "model": model,
        },
    )


@login_required
def ConfirmaOrdenTaller(request, ordenprimaria_id):
    Orden = OrdenPrimaria.objects.filter(centro=request.user.trabajador.centro)
    modelComercial = Orden.filter(confComercial=False)
    cantidad = modelComercial.count()
    modelTaller = Orden.filter(confComercial=True).filter(confTaller=False)
    cantidad1 = modelTaller.count()
    # model=OrdenPrimaria.objects.filter(centro=request.user.trabajador.centro).filter(fecha_entrada_taller=None).filter(id=ordenprimaria_id)
    model = get_object_or_404(OrdenPrimaria, id=ordenprimaria_id)
    return render(
        request,
        "Miscelaneos/confirmaordentaller.html",
        {
            "cantidad": cantidad,
            "modelComercial": modelComercial,
            "cantidad1": cantidad1,
            "modelTaller": modelTaller,
            "model": model,
        },
    )


class TrabajosDiarios(ListadoOrdenesMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dt = datetime.datetime.now()
        last_y = dt.year
        last_m = dt.month
        last_d = dt.day
        model_creadas = (
            self.object_list.filter(fecha_creacion__year=last_y)
            .filter(fecha_creacion__month=last_m)
            .filter(fecha_creacion__day=last_d)
        )
        model_reparadas = (
            self.object_list.filter(fecha_defectacion__year=last_y)
            .filter(fecha_defectacion__month=last_m)
            .filter(fecha_defectacion__day=last_d)
        )
        model_cerradas = (
            self.object_list.filter(fecha_cierre__year=last_y)
            .filter(fecha_cierre__month=last_m)
            .filter(fecha_cierre__day=last_d)
        )
        context["model_creadas"] = model_creadas
        context["model_reparadas"] = model_reparadas
        context["model_cerradas"] = model_cerradas
        return context


@login_required
def ordenesEdades(request):
    xOrden = []
    xDias = []
    yOrden = []
    yDias = []
    zOrden = []
    zDias = []
    xFecha = datetime.datetime.now()
    xFecha = datetime.datetime.strftime(xFecha, "%d/%m/%Y")
    xFecha = datetime.datetime.strptime(xFecha, "%d/%m/%Y")
    Orden = OrdenPrimaria.objects.filter(centro=request.user.trabajador.centro).filter(
        cerrada=False
    )
    modelComercial = Orden.filter(confComercial=False)
    cantidad = modelComercial.count()
    modelTaller = Orden.filter(confComercial=True).filter(confTaller=False)
    cantidad1 = modelTaller.count()
    xPendiente = Orden.filter(estado=get_object_or_404(Estado, pk=2))
    for orden in xPendiente:
        fecha = orden.fecha_entrada_taller
        fecha = datetime.datetime.strftime(fecha, "%d/%m/%Y")
        fecha = datetime.datetime.strptime(fecha, "%d/%m/%Y")
        dias = (xFecha - fecha) / datetime.timedelta(days=1)
        dias = int(dias)
        if dias > 90:
            orden.tiempo = dias
            orden.save()
            zOrden.append(orden)
        elif dias > 60 and dias < 91:
            orden.tiempo = dias
            orden.save()
            yOrden.append(orden)
        else:
            orden.tiempo = dias
            orden.save()
            xOrden.append(orden)
    return render(
        request,
        "Information/ordenes_edades.html",
        {
            "cantidad": cantidad,
            "modelComercial": modelComercial,
            "cantidad1": cantidad1,
            "modelTaller": modelTaller,
            "xOrden": xOrden,
            "yOrden": yOrden,
            "zOrden": zOrden,
        },
    )


class ListSinDefectar(ListadoOrdenesMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        listado = []
        for model in self.object_list:
            fecha = model.fecha_entrada_taller
            xDias = CalcularTiempo(fecha)
            if xDias >= 7:
                model.tiempo = xDias
                model.save()
                listado.append(model)
        context["listado"] = listado
        return context

    def get_queryset(self):
        self.queryset = (
            self.get_list()
            .filter(fecha_defectacion=None)
            .exclude(fecha_entrada_taller=None)
        )
        return self.queryset


class ListSinReparar(ListadoOrdenesMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        listado = []
        for model in self.object_list:
            fecha = model.fecha_entrada_taller
            xDias = CalcularTiempo(fecha)
            if xDias >= 30:
                model.tiempo = xDias
                model.save()
                listado.append(model)
        context["listado"] = listado
        return context

    def get_queryset(self):
        self.queryset = (
            self.get_list()
            .exclude(cerrada=True)
            .exclude(estado=get_object_or_404(Estado, pk=3))
            .exclude(estado=get_object_or_404(Estado, pk=4))
            .exclude(fecha_entrada_taller=None)
        )
        return self.queryset


class WarrantyList(ListadoOrdenesMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        listado = []
        for model in self.object_list:
            fecha = model.garantia_reparacion
            xDias = CalcularTiempo(fecha)
            xDias = int(-(xDias) + 1)
            model.tiempo = xDias
            model.save()
            listado.append(model)
        context["listado"] = listado
        return context

    def get_queryset(self):
        self.queryset = self.get_list().exclude(garantia_reparacion=None)
        return self.queryset
