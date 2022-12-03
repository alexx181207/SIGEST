from .models import  OrdenPrimaria, Estado,  Tecnologia
from .views import BaseDatosMixin, CalcularTiempo
#from braces.views import PermissionRequiredMixin, CsrfExemptMixin, JsonRequestResponseMixin
#from django.contrib import messages
#from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
#from django.contrib.auth.models import User
#from django.urls import reverse_lazy
#from django.forms import ModelForm 
#from django.http import HttpResponse, JsonResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404
#from django.template.context import RequestContext
#from django.utils.decorators import method_decorator
#from django.views.generic.base import TemplateResponseMixin, View
#from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import ListView, DetailView
import datetime


class ListadoOrdenesMixin(BaseDatosMixin, ListView):
    model=OrdenPrimaria
    template_name='Information/list.html'
    tecnologia=None
    orden=None
    model1=None
    model2=None

    def get_queryset(self):
        self.orden= OrdenPrimaria.objects.filter(centro=self.request.user.trabajador.centro)
        return self.orden  

class RegistroTFA(ListadoOrdenesMixin):
    template_name='Taller/list_reg_tfa.html'
   
    def get_queryset(self):
        self.tecnologia=get_object_or_404(Tecnologia, pk=1)
        self.orden= OrdenPrimaria.objects.filter(centro=self.request.user.trabajador.centro).filter(
            tecnologia=self.tecnologia).exclude(fecha_entrada_taller=None)
        return self.orden

class RegistroTB(RegistroTFA):
    template_name='Taller/list_reg_tb.html'
    
    def get_queryset(self):
        self.tecnologia=get_object_or_404(Tecnologia, pk=2)
        self.orden= OrdenPrimaria.objects.filter(centro=self.request.user.trabajador.centro).filter(
            tecnologia=self.tecnologia).exclude(fecha_entrada_taller=None)
        return self.orden


class ListadoPendientes(ListadoOrdenesMixin):
    template_name='Taller/list_pendientes.html'
   
    def get_queryset(self):
        self.orden=OrdenPrimaria.objects.filter(centro=self.request.user.trabajador.centro).exclude(estado=get_object_or_404(Estado, pk=3)).exclude(
            estado=get_object_or_404(Estado, pk=4)).exclude(fecha_entrada_taller=None)
        return self.orden

class ListadoReparadas(ListadoOrdenesMixin):
    template_name='Taller/list_reparadas.html'

    def get_queryset(self):
        self.orden=OrdenPrimaria.objects.filter(centro=self.request.user.trabajador.centro).exclude(cerrada=True).exclude(
            estado=get_object_or_404(Estado, pk=1)).exclude(estado=get_object_or_404(Estado, pk=2))
        return self.orden

class GestionTelefono(ListadoOrdenesMixin):
    template_name='Comercial/list_gest_tel.html'

    def get_context_data(self, **kwargs):
        context=super().get_context_data( **kwargs)
        self.model1=OrdenPrimaria.objects.filter(centro=self.request.user.trabajador.centro).exclude(cerrada=True).exclude(
            estado=get_object_or_404(Estado, pk=1)).exclude(estado=get_object_or_404(Estado, pk=2)).filter(nombre_cliente=None)
        self.model2=OrdenPrimaria.objects.filter(centro=self.request.user.trabajador.centro).exclude(cerrada=True).exclude(
            estado=get_object_or_404(Estado, pk=1)).exclude(estado=get_object_or_404(Estado, pk=2)).exclude(
                nombre_cliente=None).filter(impresion=False).filter(llama=self.request.user.trabajador)
        context['model1'] = self.model1
        context['model2'] = self.model2      
        return context   

class EntregarOrdenesTaller(ListadoOrdenesMixin):
    template_name='Miscelaneos/list_sin_entregar.html'

    def get_queryset(self):
        self.orden=OrdenPrimaria.objects.filter(centro=self.request.user.trabajador.centro).filter(confComercial=False)
        return self.orden

class ConfirmarOrdenesTaller(ListadoOrdenesMixin):
    template_name='Miscelaneos/list_sin_confirmar.html'

    def get_queryset(self):
        self.orden=OrdenPrimaria.objects.filter(centro=self.request.user.trabajador.centro).filter(confComercial=True).filter(confTaller=False)
        return self.orden


"""@login_required
def EntregarOrdenesTaller(request):
    Orden=OrdenPrimaria.objects.filter(centro=request.user.trabajador.centro)
    modelComercial=Orden.filter(confComercial=False)
    cantidad=modelComercial.count()
    modelTaller=Orden.filter(confComercial=True).filter(confTaller=False)
    cantidad1=modelTaller.count()
    model = OrdenPrimaria.objects.filter(centro=request.user.trabajador.centro).filter(confComercial=False)
    return render(request, 'Comercial/list_sin_entregar.html', {'cantidad':cantidad, 'modelComercial':modelComercial, 'cantidad1':cantidad1, 'modelTaller':modelTaller, 'model': model })

@login_required
def ConfirmarOrdenesTaller(request):
    Orden=OrdenPrimaria.objects.filter(centro=request.user.trabajador.centro)
    modelComercial=Orden.filter(confComercial=False)
    cantidad=modelComercial.count()
    modelTaller=Orden.filter(confComercial=True).filter(confTaller=False)
    cantidad1=modelTaller.count()
    model = OrdenPrimaria.objects.filter(centro=request.user.trabajador.centro).filter(confComercial=True).filter(confTaller=False)
    return render(request, 'Comercial/list_sin_confirmar.html', {'cantidad':cantidad, 'modelComercial':modelComercial, 'cantidad1':cantidad1, 'modelTaller':modelTaller, 'model': model })"""

@login_required
def EntregaOrdenTaller(request, ordenprimaria_id):
    Orden=OrdenPrimaria.objects.filter(centro=request.user.trabajador.centro)
    modelComercial=Orden.filter(confComercial=False)
    cantidad=modelComercial.count()
    modelTaller=Orden.filter(confComercial=True).filter(confTaller=False)
    cantidad1=modelTaller.count()
    #model=OrdenPrimaria.objects.filter(centro=request.user.trabajador.centro).filter(fecha_entrada_taller=None).filter(id=ordenprimaria_id)
    model = get_object_or_404(OrdenPrimaria, id=ordenprimaria_id)
    return render(request, 'Miscelaneos/orden_sin_entregar.html', {'cantidad':cantidad, 'modelComercial':modelComercial, 'cantidad1':cantidad1, 'modelTaller':modelTaller, 'model': model})

@login_required
def ConfirmaOrdenTaller(request, ordenprimaria_id):
    Orden=OrdenPrimaria.objects.filter(centro=request.user.trabajador.centro)
    modelComercial=Orden.filter(confComercial=False)
    cantidad=modelComercial.count()
    modelTaller=Orden.filter(confComercial=True).filter(confTaller=False)
    cantidad1=modelTaller.count()
    #model=OrdenPrimaria.objects.filter(centro=request.user.trabajador.centro).filter(fecha_entrada_taller=None).filter(id=ordenprimaria_id)
    model = get_object_or_404(OrdenPrimaria, id=ordenprimaria_id)
    return render(request, 'Miscelaneos/orden_sin_confirmar.html', {'cantidad':cantidad, 'modelComercial':modelComercial, 'cantidad1':cantidad1, 'modelTaller':modelTaller, 'model': model})


class TrabajosDiarios(ListadoOrdenesMixin):
    template_name='Information/trabajos_diarios.html'

    def get_context_data(self, **kwargs):
        context=super().get_context_data( **kwargs)
        dt=datetime.datetime.now()
        last_y=dt.year
        last_m=dt.month
        last_d=dt.day
        model_creadas=self.object_list.filter(fecha_creacion__year=last_y).filter(fecha_creacion__month=last_m).filter(
            fecha_creacion__day=last_d)
        model_reparadas=self.object_list.filter(fecha_defectacion__year=last_y).filter(fecha_defectacion__month=last_m).filter(
            fecha_defectacion__day=last_d)
        model_cerradas=self.object_list.filter(fecha_cierre__year=last_y).filter(fecha_cierre__month=last_m).filter(
            fecha_cierre__day=last_d)
        context['model_creadas'] = model_creadas
        context['model_reparadas'] = model_reparadas
        context['model_cerradas'] = model_cerradas    
        return context

    def get_queryset(self):
        self.orden=OrdenPrimaria.objects.filter(centro=self.request.user.trabajador.centro)
        return self.orden

"""@login_required
def TrabajosDiarios(request):
    Orden=OrdenPrimaria.objects.filter(centro=request.user.trabajador.centro)
    modelComercial=Orden.filter(confComercial=False)
    cantidad=modelComercial.count()
    modelTaller=Orden.filter(confComercial=True).filter(confTaller=False)
    cantidad1=modelTaller.count()
    dt=datetime.datetime.now()
    last_y=dt.year
    last_m=dt.month
    last_d=dt.day
    model_creadas = Orden.filter(fecha_creacion__year=last_y).filter(fecha_creacion__month=last_m).filter(fecha_creacion__day=last_d)
    model_reparadas= Orden.filter(fecha_defectacion__year=last_y).filter(fecha_defectacion__month=last_m).filter(fecha_defectacion__day=last_d)
    model_cerradas= Orden.filter(fecha_cierre__year=last_y).filter(fecha_cierre__month=last_m).filter(fecha_cierre__day=last_d)
    return render(request, 'Comercial/trabajos_diarios.html', {'cantidad':cantidad, 'modelComercial':modelComercial, 'cantidad1':cantidad1, 'modelTaller':modelTaller, 'model_creadas': model_creadas, 'model_reparadas': model_reparadas, 'model_cerradas': model_cerradas})"""

@login_required
def ordenesEdades(request):
    xOrden=[]
    xDias=[]
    yOrden=[]
    yDias=[]
    zOrden=[]
    zDias=[]
    xFecha=datetime.datetime.now()
    xFecha=datetime.datetime.strftime(xFecha, '%d/%m/%Y')
    xFecha=datetime.datetime.strptime(xFecha, '%d/%m/%Y')
    Orden=OrdenPrimaria.objects.filter(centro=request.user.trabajador.centro).filter(cerrada=False)
    modelComercial=Orden.filter(confComercial=False)
    cantidad=modelComercial.count()
    modelTaller=Orden.filter(confComercial=True).filter(confTaller=False)
    cantidad1=modelTaller.count()
    xPendiente=Orden.filter(estado=get_object_or_404(Estado, pk=2))
    for orden in xPendiente:
        fecha=orden.fecha_entrada_taller
        fecha=datetime.datetime.strftime(fecha, '%d/%m/%Y')
        fecha=datetime.datetime.strptime(fecha, '%d/%m/%Y')
        dias=(xFecha-fecha)/datetime.timedelta(days=1)
        dias=int(dias)
        if (dias>90):
            orden.tiempo=dias
            orden.save()
            zOrden.append(orden)
        elif (dias > 60 and dias < 91):
            orden.tiempo=dias
            orden.save()
            yOrden.append(orden)
        else:
            orden.tiempo=dias
            orden.save()
            xOrden.append(orden)
    return render(request, 'Information/ordenes_edades.html', {'cantidad':cantidad, 'modelComercial':modelComercial, 'cantidad1':cantidad1, 'modelTaller':modelTaller, 'xOrden':xOrden, 'yOrden':yOrden, 'zOrden':zOrden} )
    
class sDefectarfTiempo(ListadoOrdenesMixin):
    template_name='Information/list_sin_defectar.html'


    def get_context_data(self, **kwargs):
        context=super().get_context_data( **kwargs)
        listado=[]
        for model in self.object_list:
            fecha=model.fecha_entrada_taller
            xDias=CalcularTiempo(fecha)
            if xDias >= 7:
                model.tiempo=xDias
                model.save()
                listado.append(model)
        context['listado'] = listado    
        return context

    def get_queryset(self):
        self.orden=OrdenPrimaria.objects.filter(centro=self.request.user.trabajador.centro).filter(
            fecha_defectacion=None).exclude(fecha_entrada_taller=None)
        return self.orden

class sRepararfTiempo(ListadoOrdenesMixin):
    template_name='Information/list_sin_reparar.html'

    def get_context_data(self, **kwargs):
        context=super().get_context_data( **kwargs)
        listado=[]
        for model in self.object_list:
            fecha=model.fecha_entrada_taller
            xDias=CalcularTiempo(fecha)
            if xDias >= 30:
                model.tiempo=xDias
                model.save()
                listado.append(model)
        context['listado'] = listado    
        return context

    def get_queryset(self):
        self.orden=OrdenPrimaria.objects.filter(centro=self.request.user.trabajador.centro).exclude(cerrada=True).exclude(
            estado=get_object_or_404(Estado, pk=3)).exclude(estado=get_object_or_404(Estado, pk=4)).exclude(fecha_entrada_taller=None)
        return self.orden

class EquipmentWarr(ListadoOrdenesMixin):
    template_name='Information/warranty_list.html'

    def get_context_data(self, **kwargs):
        context=super().get_context_data( **kwargs)
        listado=[]
        for model in self.object_list:
            fecha=model.garantia_reparacion
            xDias=CalcularTiempo(fecha)
            xDias=int(-(xDias)+1)
            model.tiempo=xDias
            model.save()
            listado.append(model)
        context['listado'] = listado    
        return context

    def get_queryset(self):
        self.orden=OrdenPrimaria.objects.filter(centro=self.request.user.trabajador.centro).exclude(garantia_reparacion=None)
        return self.orden

