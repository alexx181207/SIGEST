#import os
from .forms import LoginForm #, DefectarModel, BuscarOrdenForm, BuscarServicioForm
from .models import (OrdenPrimaria, Modelo, Defecto, Estado,  Recursos,
    Tecnologia, Prefijo, OrdenHistorico, ReporteGestionImpreso, ManoObra, Consumo_Recursos)

#from braces.views import PermissionRequiredMixin
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
#from django.contrib.auth.models import User
from django.urls import reverse_lazy
#from django.forms import ModelForm 
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
#from django.template import Context
#from django.template.context import RequestContext
from django.utils.decorators import method_decorator
#from django.views.generic.base import TemplateResponseMixin, View
#from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
#from django.views.generic.list import ListView
from django.views.generic.base import View, TemplateView
from .files_views import render_to_pdf
import datetime
from django.utils import timezone
#from django.views.decorators.csrf import csrf_protect
#import json
#from io import StringIO
#from django.template.loader import get_template
#from xhtml2pdf import pisa
#import cgi
from django.template.loader import render_to_string


def CalcularTiempo(fecha):
    fechaActual=datetime.datetime.now()
    fechaActual=datetime.datetime.strftime(fechaActual, '%d/%m/%Y')
    fechaActual=datetime.datetime.strptime(fechaActual, '%d/%m/%Y')
    fecha=datetime.datetime.strftime(fecha, '%d/%m/%Y')
    fecha=datetime.datetime.strptime(fecha, '%d/%m/%Y')
    dias=(fechaActual-fecha)/datetime.timedelta(days=1)
    dias += 1
    return int(dias)




class BaseDatosMixin(LoginRequiredMixin, View):
    orden=None  

    def get_context_data(self, **kwargs):
        context=super().get_context_data( **kwargs)
        modelComercial=OrdenPrimaria.objects.filter(centro=self.request.user.trabajador.centro).filter(confComercial=False)
        cantidad=modelComercial.count()
        modelTaller=OrdenPrimaria.objects.filter(centro=self.request.user.trabajador.centro).filter(confComercial=True).filter(confTaller=False)
        cantidad1=modelTaller.count()
        context['cantidad'] = cantidad
        context['modelComercial'] = modelComercial
        context['cantidad1'] = cantidad1
        context['modelTaller'] = modelTaller
        return context



class Index(BaseDatosMixin, TemplateView):
    template_name="Miscelaneos/index.html"

    def get_context_data(self, **kwargs):
        context=super().get_context_data( **kwargs)
        Orden=OrdenPrimaria.objects.filter(centro=self.request.user.trabajador.centro).filter(cerrada=False)
        cant_defec_tfa=Orden.filter(tecnologia=get_object_or_404(Tecnologia, pk=1)).filter(estado=get_object_or_404(Estado, pk=1)).count()
        cant_rep_tfa=Orden.filter(tecnologia=get_object_or_404(Tecnologia, pk=1)).filter(estado=get_object_or_404(Estado, pk=3)).count()
        cant_irrep_tfa=Orden.filter(tecnologia=get_object_or_404(Tecnologia, pk=1)).filter(estado=get_object_or_404(Estado, pk=4)).count()
        cant_pend_tfa=Orden.filter(tecnologia=get_object_or_404(Tecnologia, pk=1)).filter(estado=get_object_or_404(Estado, pk=2)).count()
        cant_defec_tb=Orden.filter(tecnologia=get_object_or_404(Tecnologia, pk=2)).filter(estado=get_object_or_404(Estado, pk=1)).count()
        cant_rep_tb=Orden.filter(tecnologia=get_object_or_404(Tecnologia, pk=2)).filter(estado=get_object_or_404(Estado, pk=3)).count()
        cant_irrep_tb=Orden.filter(tecnologia=get_object_or_404(Tecnologia, pk=2)).filter(estado=get_object_or_404(Estado, pk=4)).count()
        cant_pend_tb=Orden.filter(tecnologia=get_object_or_404(Tecnologia, pk=2)).filter(estado=get_object_or_404(Estado, pk=2)).count()
        context['cant_defec_tfa'] = cant_defec_tfa
        context['cant_rep_tfa'] = cant_rep_tfa
        context['cant_irrep_tfa'] = cant_irrep_tfa
        context['cant_pend_tfa'] = cant_pend_tfa
        context['cant_defec_tb'] = cant_defec_tb
        context['cant_rep_tb'] = cant_rep_tb
        context['cant_irrep_tb'] = cant_irrep_tb
        context['cant_pend_tb'] = cant_pend_tb
        return context


class PdfView(BaseDatosMixin, PermissionRequiredMixin, TemplateView):
    permission_required='Taller.add_ordenrimaria'

    def get(self, request, plantilla, *args, **kwargs):
        #pdf=render_to_pdf("orden/orden_trabajo.html")
        modelo=OrdenPrimaria.objects.filter(ordena=request.user.trabajador.codigo_siprec)
        for modelo in modelo:
            orden_id=modelo.id
        model=get_object_or_404(OrdenPrimaria, id=orden_id)
        context=super().get_context_data( **kwargs)
        context['model']=model
        return render(request, plantilla, context)



@login_required
def pdf_view(request, plantilla):
    Orden=OrdenPrimaria.objects.filter(centro=request.user.trabajador.centro).filter(cerrada=False)
    modelComercial=Orden.filter(confComercial=False)
    cantidad=modelComercial.count()
    modelTaller=Orden.filter(confComercial=True).filter(confTaller=False)
    cantidad1=modelTaller.count()
    modelo=OrdenPrimaria.objects.filter(ordena=request.user.trabajador.codigo_siprec)
    for model in modelo:
        orden_id=model.id
        model=get_object_or_404(OrdenPrimaria, id=orden_id)
    return render (request, plantilla, {'cantidad':cantidad, 'modelComercial':modelComercial, 'cantidad1':cantidad1, 'modelTaller':modelTaller,'model':model})



class PDFOrden(View):
    """
    Regresa PDF basando en template Django/HTML
    """
    def get(self, request, plantilla, *args, **kwargs):
        #pdf=render_to_pdf("orden/orden_trabajo.html")
        modelo=OrdenPrimaria.objects.filter(ordena=request.user.trabajador.codigo_siprec)
        for model in modelo:
            orden_id=model.id
        model=get_object_or_404(OrdenPrimaria, id=orden_id)
        pdf=render_to_pdf(plantilla, {'model':model})
        return HttpResponse(pdf, content_type="application/pdf")

class PDFGestion(LoginRequiredMixin, View):
    """
    Regresa PDF basando en template Django/HTML
    """
    def get(self, request, *args, **kwargs):
        #pdf=render_to_pdf("orden/orden_trabajo.html")
        user=request.user
        model=OrdenPrimaria.objects.filter(centro=request.user.trabajador.centro).exclude(cerrada=True).exclude(estado=get_object_or_404(Estado, pk=1)).exclude(estado=get_object_or_404(Estado, pk=2)).exclude(nombre_cliente=None).filter(impresion=False).filter(llama=request.user.trabajador)
        reporte_gestion=ReporteGestionImpreso.objects.create(reporta=user.trabajador)
        for modelo in model:
            reporte_gestion.ordenes.add(modelo)
            modelo.impresion=True
            modelo.save()
        reporte_gestion.save()   
        pdf=render_to_pdf("orden/gest_reparada.html", {'model':model, 'user':user})
        return HttpResponse(pdf, content_type="application/pdf")

def loggin(request):
    return HttpResponseRedirect("/accounts/login/")


def user_login(request):
    modelComercial=None 
    modelTaller=None  
    if request.method=='POST':
        form=LoginForm(request.POST)
        if form.is_valid():
            cd=form.cleaned_data
            user=authenticate(username=cd['username'], password = cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    messages.add_message(request, messages.INFO, 'Usuario autenticado satisfactoriamente')
                    if user.has_perm('Taller.add_ordenprimaria'):
                        comercial_user=True
                    else:
                        comercial_user=False
                    if user.has_perm('Taller.add_ordenhistorico'):
                        taller_user=True
                    else:
                        taller_user=False
                    Orden=OrdenPrimaria.objects.filter(centro=request.user.trabajador.centro).filter(cerrada=False)
                    modelComercial=Orden.filter(confComercial=False)
                    cantidad=modelComercial.count()
                    modelTaller=Orden.filter(confComercial=True).filter(confTaller=False)
                    cantidad1=modelTaller.count()
                    cant_defec_tfa=Orden.filter(tecnologia=get_object_or_404(Tecnologia, pk=2)).filter(estado=get_object_or_404(Estado, pk=1)).count()
                    cant_pend_tfa=Orden.filter(tecnologia=get_object_or_404(Tecnologia, pk=2)).filter(estado=get_object_or_404(Estado, pk=2)).count()
                    cant_rep_tfa=Orden.filter(tecnologia=get_object_or_404(Tecnologia, pk=2)).filter(estado=get_object_or_404(Estado, pk=3)).count()
                    cant_irrep_tfa=Orden.filter(tecnologia=get_object_or_404(Tecnologia, pk=2)).filter(estado=get_object_or_404(Estado, pk=4)).count()
                    cant_defec_tb=Orden.filter(tecnologia=get_object_or_404(Tecnologia, pk=1)).filter(estado=get_object_or_404(Estado, pk=1)).count()
                    cant_pend_tb=Orden.filter(tecnologia=get_object_or_404(Tecnologia, pk=1)).filter(estado=get_object_or_404(Estado, pk=2)).count()
                    cant_rep_tb=Orden.filter(tecnologia=get_object_or_404(Tecnologia, pk=1)).filter(estado=get_object_or_404(Estado, pk=3)).count()
                    cant_irrep_tb=Orden.filter(tecnologia=get_object_or_404(Tecnologia, pk=1)).filter(estado=get_object_or_404(Estado, pk=4)).count()
                return render(request, 'Miscelaneos/index.html', {'cantidad':cantidad, 'modelComercial':modelComercial, 'cantidad1':cantidad1, 'modelTaller':modelTaller,'cant_defec_tfa':cant_defec_tfa, 'cant_pend_tfa':cant_pend_tfa, 
                    'cant_rep_tfa':cant_rep_tfa, 'cant_irrep_tfa':cant_irrep_tfa,'cant_defec_tb':cant_defec_tb, 'cant_pend_tb':cant_pend_tb, 'cant_rep_tb':cant_rep_tb, 'cant_irrep_tb':cant_irrep_tb, 'comercial_user':comercial_user, 'taller_user':taller_user,'form': form })
            else:
                messages.add_message(request, messages.INFO, 'Sus credenciales no son válidas, si no recuerda su contraseña contacte con el administrador')
                form=LoginForm()
    else:
        form=LoginForm()
    return render(request, 'Authentication/login.html', {'form': form})

                    

@login_required
def loggedout(request):
    logout(request)
    return HttpResponseRedirect("/./")



@login_required
def buscarservicio(request):
    error = False
    Orden=OrdenPrimaria.objects.filter(centro=request.user.trabajador.centro)
    modelComercial=Orden.filter(confComercial=False)
    cantidad=modelComercial.count()
    modelTaller=Orden.filter(confComercial=True).filter(confTaller=False)
    cantidad1=modelTaller.count()
    if 'q' in request.GET:
        q = request.GET['q']
        if not q:
            error=True
        else:
            model=Orden.filter(servicio= q)
    if 'p' in request.GET:
        p = request.GET['p']
        if 'r' in request.GET:
            r=request.GET['r']
            if not p and r:
                error=True
            else:
                model=model.filter(fecha_creacion__range=(p, r))
                return render(request, 'Information/serviciobuscar_form.html', {'cantidad':cantidad, 'modelComercial':modelComercial, 'cantidad1':cantidad1, 'modelTaller':modelTaller, 'model': model})

    return render(request, 'Information/serviciobuscar_form.html', {'cantidad':cantidad, 'modelComercial':modelComercial, 'cantidad1':cantidad1, 'modelTaller':modelTaller, 'error': error})

def reimprimir_orden(request, plantilla, ordenprimaria_id):
    Orden=OrdenPrimaria.objects.filter(centro=request.user.trabajador.centro)
    modelComercial=Orden.filter(confComercial=False)
    cantidad=modelComercial.count()
    modelTaller=Orden.filter(confComercial=True).filter(confTaller=False)
    cantidad1=modelTaller.count()
    for model in Orden:
        model=get_object_or_404(Orden, id=ordenprimaria_id)
    return render (request, plantilla, {'cantidad':cantidad, 'modelComercial':modelComercial, 'cantidad1':cantidad1, 'modelTaller':modelTaller,'model':model})
    



class CrearOrden(BaseDatosMixin, PermissionRequiredMixin, CreateView):    
    model=OrdenPrimaria
    modelact=None
    template_name='Comercial/ordenprimaria_form.html'
    #success_url = render_to_pdf(request, 'orden/orden_trabajo.html',{'modelact': modelact})
    success_url=reverse_lazy('pdf_orden')
    permission_required='Comercial.add_ordenprimaria'
    fields = ['prefijo', 'servicio', 'modelo', 'defecto', 'serie',  'nombre_cliente_entrega', 'direccion_cliente_entrega','ci_cliente_entrega', 'contacto_telefono', 'propietario', 'folio_venta', 'fecha_venta', 'garantia', 'fecha_vencimiento_garantia', 'observaciones']

    def get_context_data(self, **kwargs):
        context=super().get_context_data( **kwargs)
        context['defec'] = Defecto.objects.all()
        context['mod'] = Modelo.objects.all()
        context['prefijo'] = Prefijo.objects.all()
        return context


    def dispatch(self, request, *args, **kwargs):
        if request.method=='POST':
            messages.add_message(request, messages.INFO, 'La orden fue creada con éxito')
        return super(CrearOrden, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):   
        d=datetime.datetime.now()
        last_d=d.year
        last_m=d.month
        user = self.request.user
        centro=user.trabajador.centro
        estado = get_object_or_404(Estado, pk=1)
        self.object = form.save(commit=False)       
        temp=1
        ordenp = OrdenPrimaria.objects.all()
        ordenp.order_by('No_orden')
        for orden in ordenp:
            fe=orden.fecha_creacion
            if fe.year==last_d and fe.month==last_m:
                temp+=1               
            else:
                temp=1   

        self.object.No_orden = '%s%s%s' %(str(last_d), str(last_m),str(temp))
        self.object.centro=centro
        self.object.ordena = user.trabajador.codigo_siprec
        self.object.fecha_creacion=datetime.datetime.now()
        self.object.estado=estado
        self.object.tecnologia=self.object.modelo.tecnologia
        #self.object.codigo_sap=self.object.modelo.codigo_sap
        #self.object.descripcion=self.object.modelo.descripcion
        self.object=form.save() 
               
        #modelact=get_object_or_404(OrdenPrimaria, pk=self.object.pk)
        return super(CrearOrden, self).form_valid(form)


class RepararOrden(BaseDatosMixin, PermissionRequiredMixin, UpdateView):
    modelprim=None
    model=OrdenPrimaria
    success_url = reverse_lazy('ordenes_pendientes')
    permission_required='Taller.add_ordenhistorico'
    template_name = 'Taller/ordenreparada_form.html'
    fields = ['accion_reparacion', 'estado', 'mano_obra'] 

    
    def get_context_data(self,**kwargs):
        context=super().get_context_data( **kwargs)
        estado=Estado.objects.exclude(pk=1)
        recursos=Recursos.objects.all()
        mano_obra=ManoObra.objects.all()
        context['estado'] = estado
        context['recursos'] = recursos
        context['mano_obra'] = mano_obra
        return context

    def dispatch(self, request, pk, *args, **kwargs):
        self.modelprim=get_object_or_404(OrdenPrimaria, id=pk)
        if request.method=='POST':
            messages.add_message(request, messages.INFO, 'La reparación se ha efectuado de manera satisfactoria')
        return super(RepararOrden, self).dispatch(request, pk, *args, **kwargs)


    def form_valid(self, form):
        user = self.request.user
        centro=user.trabajador.centro
        self.object = form.save(commit=False)
        self.object.fecha_defectacion=datetime.datetime.now()
        self.object.repara=user.trabajador.codigo_siprec
        modelo=Consumo_Recursos.objects.filter(centro=user.trabajador.centro).filter(asociado_orden=False)
        for modelo in modelo:
            self.object.consumo_recursos.add(modelo)
            modelo.asociado_orden=True
            modelo.save()
        
        orden_hist=OrdenHistorico.objects.create(orden_reparada=self.object, centro=centro, prefijo=self.object.prefijo.nombre, fecha_defectacion=self.object.fecha_defectacion,
        accion_reparacion=self.object.accion_reparacion, estado_defectadas=self.object.estado, servicio=self.object.servicio)
        orden_hist.save()
        self.object = form.save()
        return super(RepararOrden, self).form_valid(form)
       



class CerrarOrden(BaseDatosMixin, PermissionRequiredMixin, UpdateView):
    model = OrdenPrimaria
    success_url = reverse_lazy('ordenes_reparadas')
    template_name = 'Comercial/ordencerrada_form.html'
    permission_required='Comercial.add_ordenprimaria'
    fields = ['nombre_cliente_recibe', 'direccion_cliente_recibe', 'ci_cliente_recibe']

    @method_decorator(login_required)
    def dispatch(self, request, pk, *args, **kwargs):
        if request.method=='POST':
            messages.add_message(request, messages.INFO, 'La orden se ha cerrado con éxito')          
        return super(CerrarOrden, self).dispatch(request, pk, *args, **kwargs)

    def form_valid(self, form):
        user = self.request.user
        if self.object.fecha_gestion==None:
            self.object.fecha_gestion=datetime.datetime.now()
        self.object=form.save(commit=False)
        self.object.cerrada=True
        now=timezone.now()
        now=datetime.datetime.strftime(now, '%d/%m/%Y')
        now=datetime.datetime.strptime(now, '%d/%m/%Y')
        fechastr=datetime.datetime.strftime(self.object.fecha_gestion, '%d/%m/%Y')
        fechaCalulo=datetime.datetime.strptime(fechastr, '%d/%m/%Y')
        fecha=(now-fechaCalulo)/datetime.timedelta(days=1)
        if fecha < 15 :
            self.object.garantia_reparacion=now+datetime.timedelta(days=30)
        else:
            self.object.garantia_reparacion=fecha_gestion+datetime.timedelta(days=45)

        self.object.cierra = user.trabajador.codigo_siprec
        self.object.fecha_cierre=datetime.datetime.now()
        self.object=form.save()       
        return super(CerrarOrden, self).form_valid(form)


class OrdenLlamada(BaseDatosMixin, PermissionRequiredMixin, UpdateView):
    modelreparada=None
    model = OrdenPrimaria
    success_url = reverse_lazy('gestion_telefono')
    template_name = 'Comercial/ordenllamada_form.html'
    permission_required='Comercial.add_ordenprimaria'
    fields = ['nombre_cliente']

    
    @method_decorator(login_required)
    def dispatch(self, request, pk, *args, **kwargs): 
        if request.method=='POST':
            messages.add_message(request, messages.INFO, 'Se ha confirmado la gestión de esta orden con el cliente')          
        return super(OrdenLlamada, self).dispatch(request, pk, *args, **kwargs)

    def form_valid(self, form):
        user = self.request.user
        self.object=form.save(commit=False)
        self.object.llama = user.trabajador
        self.object.fecha_gestion=timezone.now()
        self.object.garantia_reparacion=datetime.datetime.now()+datetime.timedelta(days=15)
        self.object=form.save()       
        return super(OrdenLlamada, self).form_valid(form)

class ChangePassword(PasswordChangeView):
    success_url = reverse_lazy('index')
    template_name = "registration/password_change_form.html"

class OrderwarrantyView(BaseDatosMixin):
    pass



    
    


	