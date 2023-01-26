from django.contrib import admin
from .models import (
    OrdenHistorico,
)


# Register your models here.

class OrdenHistoricoAdmin(admin.ModelAdmin):
    list_display = [
        "orden_reparada",
        "prefijo",
        "servicio",
        "centro",
        "fecha_defectacion",
        "accion_reparacion",
        "estado_defectadas",
    ]
    ordering = ["fecha_defectacion"]

admin.site.register(OrdenHistorico, OrdenHistoricoAdmin)

