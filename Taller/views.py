# import os
from .forms import (
    #LoginForm,
    #PrimaryOrderForm,
    RepairForm,
    #TalkForm,
    #CloseOrderForm,
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
from .models import OrdenHistorico
from Comercial.models import OrdenPrimaria, ReporteGestionImpreso

from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.base import View, TemplateView
from .files_views import render_to_pdf
import datetime
from django.utils import timezone
from base.views import BaseDatosMixin, CalcularTiempo

# from django.views.decorators.csrf import csrf_protect
# import json
# from io import StringIO
# from django.template.loader import get_template
# from xhtml2pdf import pisa
# import cgi
from django.template.loader import render_to_string



class Index(BaseDatosMixin, TemplateView):
    template_name = "Miscelaneos/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        Orden = OrdenPrimaria.objects.filter(
            centro=self.request.user.trabajador.centro
        ).filter(cerrada=False)
        cant_defec_tfa = (
            Orden.filter(tecnologia=get_object_or_404(Tecnologia, pk=1))
            .filter(estado=get_object_or_404(Estado, pk=1))
            .count()
        )
        cant_rep_tfa = (
            Orden.filter(tecnologia=get_object_or_404(Tecnologia, pk=1))
            .filter(estado=get_object_or_404(Estado, pk=3))
            .count()
        )
        cant_irrep_tfa = (
            Orden.filter(tecnologia=get_object_or_404(Tecnologia, pk=1))
            .filter(estado=get_object_or_404(Estado, pk=4))
            .count()
        )
        cant_pend_tfa = (
            Orden.filter(tecnologia=get_object_or_404(Tecnologia, pk=1))
            .filter(estado=get_object_or_404(Estado, pk=2))
            .count()
        )
        cant_defec_tb = (
            Orden.filter(tecnologia=get_object_or_404(Tecnologia, pk=2))
            .filter(estado=get_object_or_404(Estado, pk=1))
            .count()
        )
        cant_rep_tb = (
            Orden.filter(tecnologia=get_object_or_404(Tecnologia, pk=2))
            .filter(estado=get_object_or_404(Estado, pk=3))
            .count()
        )
        cant_irrep_tb = (
            Orden.filter(tecnologia=get_object_or_404(Tecnologia, pk=2))
            .filter(estado=get_object_or_404(Estado, pk=4))
            .count()
        )
        cant_pend_tb = (
            Orden.filter(tecnologia=get_object_or_404(Tecnologia, pk=2))
            .filter(estado=get_object_or_404(Estado, pk=2))
            .count()
        )
        totalDefec = cant_defec_tfa + cant_defec_tb
        totalPend = cant_pend_tfa + cant_pend_tb
        totalReparado = cant_rep_tfa + cant_rep_tb
        totalIrrep = cant_irrep_tb + cant_irrep_tfa
        context["cant_defec_tfa"] = cant_defec_tfa
        context["cant_rep_tfa"] = cant_rep_tfa
        context["cant_irrep_tfa"] = cant_irrep_tfa
        context["cant_pend_tfa"] = cant_pend_tfa
        context["cant_defec_tb"] = cant_defec_tb
        context["cant_rep_tb"] = cant_rep_tb
        context["cant_irrep_tb"] = cant_irrep_tb
        context["cant_pend_tb"] = cant_pend_tb
        context["totalDefec"] = totalDefec
        context["totalPend"] = totalPend
        context["totalReparado"] = totalReparado
        context["totalIrrep"] = totalIrrep
        return context


"""@login_required
def buscarservicio(request):
    error = False
    Orden = OrdenPrimaria.objects.filter(centro=request.user.trabajador.centro)
    modelComercial = Orden.filter(confComercial=False)
    cantidad = modelComercial.count()
    modelTaller = Orden.filter(confComercial=True).filter(confTaller=False)
    cantidad1 = modelTaller.count()
    if "q" in request.GET:
        q = request.GET["q"]
        if not q:
            error = True
        else:
            model = Orden.filter(servicio=q)
    if "p" in request.GET:
        p = request.GET["p"]
        if "r" in request.GET:
            r = request.GET["r"]
            if not p and r:
                error = True
            else:
                model = model.filter(fecha_creacion__range=(p, r))
                return render(
                    request,
                    "Information/serviciobuscar_form.html",
                    {
                        "cantidad": cantidad,
                        "modelComercial": modelComercial,
                        "cantidad1": cantidad1,
                        "modelTaller": modelTaller,
                        "model": model,
                    },
                )

    return render(
        request,
        "Information/serviciobuscar_form.html",
        {
            "cantidad": cantidad,
            "modelComercial": modelComercial,
            "cantidad1": cantidad1,
            "modelTaller": modelTaller,
            "error": error,
        },
    )"""

class RepararOrden(BaseDatosMixin, PermissionRequiredMixin, UpdateView):
    # modelprim = None
    model = OrdenPrimaria
    form_class = RepairForm
    success_url = reverse_lazy("ordenes_pendientes")
    permission_required = "Taller.add_ordenhistorico"
    template_name = "Taller/ordenreparada_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        estado = Estado.objects.exclude(pk=1)
        recursos = Recursos.objects.all()
        mano_obra = ManoObra.objects.all()
        context["estado"] = estado
        context["recursos"] = recursos
        context["mano_obra"] = mano_obra
        return context

    def dispatch(self, request, pk, *args, **kwargs):
        # self.modelprim = get_object_or_404(OrdenPrimaria, id=pk)
        if request.method == "POST":
            messages.add_message(
                request,
                messages.INFO,
                "La reparación se ha efectuado de manera satisfactoria",
            )
        return super(RepararOrden, self).dispatch(request, pk, *args, **kwargs)

    def form_valid(self, form):
        user = self.request.user
        centro = user.trabajador.centro
        self.object = form.save(commit=False)
        self.object.fecha_defectacion = datetime.datetime.now()
        self.object.repara = user.trabajador
        modelo = Consumo_Recursos.objects.filter(centro=user.trabajador.centro).filter(
            asociado_orden=False
        )
        for modelo in modelo:
            self.object.consumo_recursos.add(modelo)
            modelo.asociado_orden = True
            modelo.save()

        orden_hist = OrdenHistorico.objects.create(
            orden_reparada=self.object,
            centro=centro,
            prefijo=self.object.prefijo.nombre,
            fecha_defectacion=self.object.fecha_defectacion,
            accion_reparacion=self.object.accion_reparacion,
            estado_defectadas=self.object.estado,
            servicio=self.object.servicio,
        )
        orden_hist.save()
        self.object = form.save()
        return super(RepararOrden, self).form_valid(form)


class ChangePassword(PasswordChangeView):
    success_url = reverse_lazy("index")
    template_name = "registration/password_change_form.html"


class OrderwarrantyView(BaseDatosMixin):
    pass
