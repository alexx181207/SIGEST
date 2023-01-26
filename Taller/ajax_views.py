from Comercial.models import OrdenPrimaria
from .models import OrdenHistorico 
from base.models import Prefijo, Consumo_Recursos, Recursos
from base.views import BaseDatosMixin
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404
import datetime
import json


class BuscarServicios(BaseDatosMixin, TemplateView):
    template_name = "Information/serviciobuscar_form.html"
    # permission_required='Taller.add_ordenprimaria'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["prefijo"] = Prefijo.objects.all()
        return context


@login_required
def buscarservicio(request):
    # if not request.is_ajax() or request.method != 'POST':
    #    return HttpResponseBadRequest('<h1>%s</h1>' % 'bad_request')
    datos = json.loads(request.POST.get("data"))
    model = OrdenPrimaria.objects.filter(servicio=datos["servicio"]).filter(
        fecha_creacion__range=(datos["fechainicio"], datos["fechafin"])
    )
    return JsonResponse({"saved": "OK"})


@login_required
def list_json(request, prefijo=None, servicio=None, fechainicio=None, fechafin=None):
    retorno = []
    fecha_inicio = ""
    fecha_fin = ""
    fecha_inirange = []
    fecha_finrange = []
    model = None

    if prefijo and servicio and fechainicio and fechafin:
        for i in fechainicio:
            if i == "/":
                fecha_inirange.append(fecha_inicio)
                fecha_inicio = ""
            else:
                fecha_inicio = fecha_inicio + i

        for u in fechafin:
            if u == "/":
                fecha_finrange.append(fecha_fin)
                fecha_fin = ""
            else:
                fecha_fin = fecha_fin + u
        fecha_inirange.append(fecha_inicio)
        fecha_finrange.append(fecha_fin)
        fecha_inidate = datetime.date(
            int(fecha_inirange[2]), int(fecha_inirange[0]), int(fecha_inirange[1])
        )
        fecha_findate = datetime.date(
            int(fecha_finrange[2]), int(fecha_finrange[0]), int(fecha_finrange[1])
        )
        # fecha_inidate=datetime.date(int(fechainicio)).strftime('%Y/%m/%d')
        # fecha_findate=datetime.date(int(fechafin)).strftime('%Y/%m/%d')
        model = (
            OrdenHistorico.objects.filter(centro=request.user.trabajador.centro)
            .filter(prefijo=prefijo)
            .filter(servicio=servicio)
            .filter(fecha_defectacion__range=(fecha_inidate, fecha_findate))
        )
        for model in model:
            retorno.append(
                {
                    "No_orden": model.orden_reparada.No_orden,
                    "servicio": model.prefijo + "" + model.servicio,
                    "fecha_creacion": model.orden_reparada.fecha_creacion.strftime(
                        "%d/%m/%Y"
                    ),
                    "modelo": model.orden_reparada.modelo.nombre,
                    "serie": model.orden_reparada.serie,
                    "accion_reparacion": model.accion_reparacion,
                    "estado": model.estado_defectadas.nombre,
                }
            )
    return JsonResponse({"data_set": retorno})


def entregar_taller(request):
    # if not request.is_ajax() or request.method != 'POST':
    #   return HttpResponseBadRequest('<h1>%s</h1>' % 'bad_request')
    datos = json.loads(request.POST.get("data"))
    modelprim = get_object_or_404(OrdenPrimaria, pk=datos["id"])
    modelprim.confComercial = True
    modelprim.entrega = request.user.trabajador
    modelprim.save()
    return JsonResponse({"saved": "OK"})


@login_required
def confirmar_taller(request):
    # if not request.is_ajax() or request.method != 'POST':
    #   return HttpResponseBadRequest('<h1>%s</h1>' % 'bad_request')
    datos = json.loads(request.POST.get("data"))
    modelprim = get_object_or_404(OrdenPrimaria, pk=datos["id"])
    modelprim.confTaller = True
    modelprim.fecha_entrada_taller = datetime.datetime.now()
    modelprim.save()
    return JsonResponse({"saved": "OK"})


@login_required
def consumir_recursos(request):
    # if not request.is_ajax() or request.method != 'POST':
    #   return HttpResponseBadRequest('<h1>%s</h1>' % 'bad_request')
    datos = json.loads(request.POST.get("data"))
    recurso = get_object_or_404(Recursos, descripcion=datos["descripcion"])
    cantidad = float(datos["cantidad"])
    importe = recurso.precio * cantidad
    consumir_recurso = Consumo_Recursos.objects.create(
        recurso=recurso,
        centro=request.user.trabajador.centro,
        fecha=datetime.datetime.now(),
        cantidad=cantidad,
        importe=importe,
        asociado_orden=False,
    )
    consumir_recurso.save()
    return JsonResponse({"saved": "OK"})


@login_required
def recursos_consumidos(request):
    retorno = []
    model = Consumo_Recursos.objects.filter(
        centro=request.user.trabajador.centro
    ).filter(asociado_orden=False)
    for model in model:
        retorno.append(
            {
                "codigo_sap": model.recurso.codigo_sap,
                "descripcion": model.recurso.descripcion,
                "fecha": model.fecha.strftime("%Y/%m/%d"),
                "precio": model.recurso.precio,
                "cantidad": model.cantidad,
                "importe": model.importe,
            }
        )
    return JsonResponse({"data_set": retorno})
