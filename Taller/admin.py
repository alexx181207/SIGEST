from django.contrib import admin
from .models import (Trabajador, OrdenPrimaria, Recursos, Estado, Modelo, Tecnologia, Defecto, 
	OrdenHistorico, Prefijo, Division_Territorial, Centro_Telecomunicaciones, Centro, ReporteGestionImpreso, ManoObra, Consumo_Recursos, Especialidad)


# Register your models here.

class TrabajadorAdmin(admin.ModelAdmin):
	list_display=['user','centro', 'codigo_siprec']
	ordering=['user']

class OrdenPrimariaAdmin(admin.ModelAdmin):
	list_display=['No_orden', 'fecha_creacion', 'centro', 'ordena', 'prefijo', 'servicio', 'tecnologia']
	ordering=['No_orden']

class EstadoAdmin(admin.ModelAdmin):
	ordering=['nombre']

class EspecialidadAdmin(admin.ModelAdmin):
	ordering=['name']

class ModeloAdmin(admin.ModelAdmin):
	list_display=['nombre', 'tecnologia', 'codigo_sap', 'descripcion']
	ordering=['nombre']

class TecnologiaAdmin(admin.ModelAdmin):
	ordering=['nombre']

class DefectoAdmin(admin.ModelAdmin):
	ordering=['nombre']

class OrdenHistoricoAdmin(admin.ModelAdmin):
	list_display=['orden_reparada', 'prefijo', 'servicio', 'centro', 'fecha_defectacion', 'accion_reparacion', 'estado_defectadas']
	ordering=['fecha_defectacion']

class RecursosAdmin(admin.ModelAdmin):
	list_display=['descripcion', 'codigo_sap', 'precio']
	ordering=['descripcion']

class Centro_TelecomunicacionesAdmin(admin.ModelAdmin):
	list_display=[ 'nombre', 'division']
	ordering=['nombre']

class CentroAdmin(admin.ModelAdmin):
	list_display=['nombre', 'centro_telecomunicaciones']
	ordering=['nombre']

class ReporteGestionImpresoAdmin(admin.ModelAdmin):
	list_display=['reporta']


class ManoObraAdmin(admin.ModelAdmin):
	list_display=['tipo', 'codigo_sap', 'precio']
	ordering=['codigo_sap']


admin.site.register(Trabajador, TrabajadorAdmin)
admin.site.register(OrdenPrimaria, OrdenPrimariaAdmin)
admin.site.register(Estado, EstadoAdmin)
admin.site.register(Modelo, ModeloAdmin)
admin.site.register(Tecnologia, TecnologiaAdmin)
admin.site.register(Defecto, DefectoAdmin)
admin.site.register(OrdenHistorico, OrdenHistoricoAdmin)
admin.site.register(Recursos, RecursosAdmin)
admin.site.register(Prefijo)
admin.site.register(Division_Territorial)
admin.site.register(Centro_Telecomunicaciones, Centro_TelecomunicacionesAdmin)
admin.site.register(Centro, CentroAdmin)
admin.site.register(ReporteGestionImpreso, ReporteGestionImpresoAdmin)
admin.site.register(ManoObra, ManoObraAdmin)
admin.site.register(Especialidad, EspecialidadAdmin)  
admin.site.register(Consumo_Recursos)