from django.contrib import admin
from .models import (
    OrdenPrimaria,
    ReporteGestionImpreso,
)


# Register your models here.


class OrdenPrimariaAdmin(admin.ModelAdmin):
    list_display = [
        "No_orden",
        "fecha_creacion",
        "centro",
        "ordena",
        "prefijo",
        "servicio",
        "tecnologia",
    ]
    ordering = ["No_orden"]


class ReporteGestionImpresoAdmin(admin.ModelAdmin):
    list_display = ["reporta"]


admin.site.register(OrdenPrimaria, OrdenPrimariaAdmin)
admin.site.register(ReporteGestionImpreso, ReporteGestionImpresoAdmin)

