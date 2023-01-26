# import os
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.base import View, TemplateView
from django.template.loader import render_to_string
import datetime
from django.utils import timezone


from .forms import (
    PrimaryOrderForm,
    TalkForm,
    CloseOrderForm,
)
from base.models import (
    Modelo,
    Defecto,
    Estado,
    Recursos,
    Tecnologia,
    Prefijo,
    ManoObra,
    Consumo_Recursos,
)
from Taller.models import OrdenHistorico 
from .models import OrdenPrimaria, ReporteGestionImpreso
from base.views import BaseDatosMixin, CalcularTiempo
from Taller.files_views import render_to_pdf

# from django.views.decorators.csrf import csrf_protect
# import json
# from io import StringIO
# from django.template.loader import get_template
# from xhtml2pdf import pisa
# import cgi




class PdfView(BaseDatosMixin, TemplateView):
    def get(self, request, plantilla, *args, **kwargs):
        # pdf=render_to_pdf("orden/orden_trabajo.html")
        modelo = OrdenPrimaria.objects.filter(ordena=request.user.trabajador)
        for modelo in modelo:
            orden_id = modelo.id
        model = get_object_or_404(OrdenPrimaria, id=orden_id)
        context = super().get_context_data(**kwargs)
        context["model"] = model
        return render(request, plantilla, context)


@login_required
def pdf_view(request, plantilla):
    Orden = OrdenPrimaria.objects.filter(centro=request.user.trabajador.centro).filter(
        cerrada=False
    )
    modelComercial = Orden.filter(confComercial=False)
    cantidad = modelComercial.count()
    modelTaller = Orden.filter(confComercial=True).filter(confTaller=False)
    cantidad1 = modelTaller.count()
    modelo = OrdenPrimaria.objects.filter(ordena=request.user.trabajador)
    for model in modelo:
        orden_id = model.id
        model = get_object_or_404(OrdenPrimaria, id=orden_id)
    return render(
        request,
        plantilla,
        {
            "cantidad": cantidad,
            "modelComercial": modelComercial,
            "cantidad1": cantidad1,
            "modelTaller": modelTaller,
            "model": model,
        },
    )


class PDFOrden(View):
    """
    Regresa PDF basando en template Django/HTML
    """

    def get(self, request, plantilla, *args, **kwargs):
        # pdf=render_to_pdf("orden/orden_trabajo.html")
        modelo = OrdenPrimaria.objects.filter(ordena=request.user.trabajador)
        for model in modelo:
            orden_id = model.id
        model = get_object_or_404(OrdenPrimaria, id=orden_id)
        pdf = render_to_pdf(plantilla, {"model": model})
        return HttpResponse(pdf, content_type="application/pdf")


class PDFGestion(LoginRequiredMixin, View):
    """
    Regresa PDF basando en template Django/HTML
    """

    def get(self, request, *args, **kwargs):
        # pdf=render_to_pdf("orden/orden_trabajo.html")
        user = request.user
        model = (
            OrdenPrimaria.objects.filter(centro=user.trabajador.centro)
            .exclude(cerrada=True)
            .exclude(nombre_cliente=None)
            .filter(impresion=False)
            .filter(llama=user.trabajador)
        )
        reporte_gestion = ReporteGestionImpreso.objects.create(reporta=user.trabajador)
        for modelo in model:
            reporte_gestion.ordenes.add(modelo)
            modelo.impresion = True
            modelo.save()
        reporte_gestion.save()
        pdf = render_to_pdf("orden/gest_reparada.html", {"model": model, "user": user})
        return HttpResponse(pdf, content_type="application/pdf")


def reimprimir_orden(request, plantilla, ordenprimaria_id):
    Orden = OrdenPrimaria.objects.filter(centro=request.user.trabajador.centro)
    modelComercial = Orden.filter(confComercial=False)
    cantidad = modelComercial.count()
    modelTaller = Orden.filter(confComercial=True).filter(confTaller=False)
    cantidad1 = modelTaller.count()
    for model in Orden:
        model = get_object_or_404(Orden, id=ordenprimaria_id)
    return render(
        request,
        plantilla,
        {
            "cantidad": cantidad,
            "modelComercial": modelComercial,
            "cantidad1": cantidad1,
            "modelTaller": modelTaller,
            "model": model,
        },
    )


class CrearOrden(BaseDatosMixin, PermissionRequiredMixin, CreateView):
    model = OrdenPrimaria
    form_class = PrimaryOrderForm
    template_name = "Comercial/ordenprimaria_form.html"
    success_url = reverse_lazy("pdf_orden")
    permission_required = "Taller.add_ordenprimaria"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["defec"] = Defecto.objects.all()
        context["mod"] = Modelo.objects.all()
        context["prefijo"] = Prefijo.objects.all()
        return context

    """def dispatch(self, request, *args, **kwargs):
        if request.method == "POST":
            messages.add_message(
                request, messages.INFO, "La orden fue creada con éxito"
            )
        return super(CrearOrden, self).dispatch(request, *args, **kwargs)"""

    def form_valid(self, form):
        d = datetime.datetime.now()
        last_d = d.year
        last_m = d.month
        user = self.request.user
        centro = user.trabajador.centro
        estado = get_object_or_404(Estado, pk=1)
        self.object = form.save(commit=False)
        temp = 1
        ordenp = OrdenPrimaria.objects.all()
        ordenp.order_by("No_orden")
        for orden in ordenp:
            fe = orden.fecha_creacion
            if fe.year == last_d and fe.month == last_m:
                temp += 1
            else:
                temp = 1

        self.object.No_orden = "%s%s%s" % (str(last_d), str(last_m), str(temp))
        self.object.centro = centro
        self.object.ordena = user.trabajador
        self.object.fecha_creacion = datetime.datetime.now()
        self.object.estado = estado
        self.object.tecnologia = self.object.modelo.tecnologia
        # self.object.codigo_sap=self.object.modelo.codigo_sap
        # self.object.descripcion=self.object.modelo.descripcion
        self.object = form.save()

        # modelact=get_object_or_404(OrdenPrimaria, pk=self.object.pk)
        return super(CrearOrden, self).form_valid(form)



class UpdateOrder(BaseDatosMixin, PermissionRequiredMixin, UpdateView):
    model = OrdenPrimaria
    template_name = "Comercial/ordenprimaria_form.html"
    success_url = reverse_lazy("list_updates")
    permission_required = "Taller.add_ordenprimaria"
    form_class = PrimaryOrderForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["defec"] = Defecto.objects.all()
        context["mod"] = Modelo.objects.all()
        context["prefijo"] = Prefijo.objects.all()
        return context

    def dispatch(self, request, *args, **kwargs):
        if request.method == "POST":
            messages.add_message(
                request, messages.INFO, "La orden fue actualizada con éxito"
            )
        return super(UpdateOrder, self).dispatch(request, *args, **kwargs)


class DeleteOrder(BaseDatosMixin, PermissionRequiredMixin, DeleteView):
    model = OrdenPrimaria
    template_name = "Comercial/delete_order.html"
    success_url = reverse_lazy("list_updates")
    permission_required = "Taller.add_ordenprimaria"


class CerrarOrden(BaseDatosMixin, PermissionRequiredMixin, UpdateView):
    model = OrdenPrimaria
    success_url = reverse_lazy("ordenes_reparadas")
    template_name = "Comercial/ordencerrada_form.html"
    permission_required = "Taller.add_ordenprimaria"
    form_class = CloseOrderForm

    @method_decorator(login_required)
    def dispatch(self, request, pk, *args, **kwargs):
        if request.method == "POST":
            messages.add_message(
                request, messages.INFO, "La orden se ha cerrado con éxito"
            )
        return super(CerrarOrden, self).dispatch(request, pk, *args, **kwargs)

    def form_valid(self, form):
        user = self.request.user
        if self.object.fecha_gestion == None:
            self.object.fecha_gestion = datetime.datetime.now()
        self.object = form.save(commit=False)
        self.object.cerrada = True
        now = timezone.now()
        now = datetime.datetime.strftime(now, "%d/%m/%Y")
        now = datetime.datetime.strptime(now, "%d/%m/%Y")
        fechastr = datetime.datetime.strftime(self.object.fecha_gestion, "%d/%m/%Y")
        fechaCalulo = datetime.datetime.strptime(fechastr, "%d/%m/%Y")
        fecha = (now - fechaCalulo) / datetime.timedelta(days=1)
        if fecha < 15:
            self.object.garantia_reparacion = now + datetime.timedelta(days=30)
        else:
            self.object.garantia_reparacion = fecha_gestion + datetime.timedelta(
                days=45
            )

        self.object.cierra = user.trabajador
        self.object.fecha_cierre = datetime.datetime.now()
        self.object = form.save()
        return super(CerrarOrden, self).form_valid(form)


class OrdenLlamada(BaseDatosMixin, PermissionRequiredMixin, UpdateView):
    model = OrdenPrimaria
    success_url = reverse_lazy("gestion_telefono")
    template_name = "Comercial/ordenllamada_form.html"
    permission_required = "Taller.add_ordenprimaria"
    form_class = TalkForm

    @method_decorator(login_required)
    def dispatch(self, request, pk, *args, **kwargs):
        if request.method == "POST":
            messages.add_message(
                request,
                messages.INFO,
                "Se ha confirmado la gestión de esta orden con el cliente",
            )
        return super(OrdenLlamada, self).dispatch(request, pk, *args, **kwargs)

    def form_valid(self, form):
        user = self.request.user
        self.object = form.save(commit=False)
        self.object.llama = user.trabajador
        self.object.fecha_gestion = timezone.now()
        self.object.garantia_reparacion = datetime.datetime.now() + datetime.timedelta(
            days=15
        )
        self.object = form.save()
        return super(OrdenLlamada, self).form_valid(form)
