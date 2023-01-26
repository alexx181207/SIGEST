from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect

from .forms import LoginForm
from Comercial.models import OrdenPrimaria
from .models import Tecnologia, Estado



def loggin(request):
    return HttpResponseRedirect("/accounts/login/")

def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd["username"], password=cd["password"])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    messages.add_message(
                        request, messages.INFO, "Usuario autenticado satisfactoriamente"
                    )
                    Orden = OrdenPrimaria.objects.filter(
                        centro=request.user.trabajador.centro
                    ).filter(cerrada=False)
                    modelComercial = Orden.filter(confComercial=False)
                    cantidad = modelComercial.count()
                    modelTaller = Orden.filter(confComercial=True).filter(
                        confTaller=False
                    )
                    cantidad1 = modelTaller.count()
                    cant_defec_tfa = (
                        Orden.filter(tecnologia=get_object_or_404(Tecnologia, pk=1))
                        .filter(estado=get_object_or_404(Estado, pk=1))
                        .count()
                    )
                    cant_pend_tfa = (
                        Orden.filter(tecnologia=get_object_or_404(Tecnologia, pk=1))
                        .filter(estado=get_object_or_404(Estado, pk=2))
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
                    cant_defec_tb = (
                        Orden.filter(tecnologia=get_object_or_404(Tecnologia, pk=2))
                        .filter(estado=get_object_or_404(Estado, pk=1))
                        .count()
                    )
                    cant_pend_tb = (
                        Orden.filter(tecnologia=get_object_or_404(Tecnologia, pk=2))
                        .filter(estado=get_object_or_404(Estado, pk=2))
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
                    totalDefec = cant_defec_tfa + cant_defec_tb
                    totalPend = cant_pend_tfa + cant_pend_tb
                    totalReparado = cant_rep_tfa + cant_rep_tb
                    totalIrrep = cant_irrep_tb + cant_irrep_tfa
                    return render(
                        request,
                        "Miscelaneos/index.html",
                        {
                            "cantidad": cantidad,
                            "modelComercial": modelComercial,
                            "cantidad1": cantidad1,
                            "modelTaller": modelTaller,
                            "cant_defec_tfa": cant_defec_tfa,
                            "cant_pend_tfa": cant_pend_tfa,
                            "cant_rep_tfa": cant_rep_tfa,
                            "cant_irrep_tfa": cant_irrep_tfa,
                            "cant_defec_tb": cant_defec_tb,
                            "cant_pend_tb": cant_pend_tb,
                            "cant_rep_tb": cant_rep_tb,
                            "cant_irrep_tb": cant_irrep_tb,
                            "totalDefec": totalDefec,
                            "totalPend": totalPend,
                            "totalReparado": totalReparado,
                            "totalIrrep": totalIrrep,
                            "form": form,
                        },
                    )
    else:
        form = LoginForm()
    return render(request, "Authentication/login.html", {"form": form})


@login_required
def loggedout(request):
    logout(request)
    return HttpResponseRedirect("/./")