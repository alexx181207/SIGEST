from django.db import models


from base.models import Centro, Estado
from Comercial.models import OrdenPrimaria



class OrdenHistorico(models.Model):
    orden_reparada = models.ForeignKey(OrdenPrimaria, on_delete=models.CASCADE)
    prefijo = models.CharField(max_length=60, null=True, blank=True)
    servicio = models.CharField(max_length=60, null=True, blank=True)
    centro = models.ForeignKey(Centro, on_delete=models.CASCADE)
    fecha_defectacion = models.DateTimeField()
    accion_reparacion = models.TextField()
    estado_defectadas = models.ForeignKey(Estado, on_delete=models.CASCADE)
