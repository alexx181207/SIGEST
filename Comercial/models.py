from django.db import models

# Create your models here.

from base.models import (
    Centro,
    Trabajador,
    Prefijo,
    Modelo,
    Tecnologia,
    Defecto,
    Estado,
    ManoObra,
    Consumo_Recursos,
)

class OrdenPrimaria(models.Model):
    """Datos iniciales de la Orden"""

    No_orden = models.CharField(max_length=50)
    fecha_creacion = models.DateTimeField()
    fecha_entrada_taller = models.DateTimeField(blank=True, null=True)
    centro = models.ForeignKey(Centro, on_delete=models.CASCADE)
    ordena = models.ForeignKey(
        Trabajador, on_delete=models.CASCADE, related_name="ordena"
    )
    """ Estos son campos nuevos"""
    folio_venta = models.CharField(max_length=80, blank=True, null=True)
    fecha_venta = models.DateTimeField(blank=True, null=True)
    # equipo=models.ForeignKey(Equipo, on_delete=models.CASCADE, blank=True, null=True)
    garantia = models.CharField(max_length=20, blank=True, null=True)
    fecha_vencimiento_garantia = models.DateTimeField(null=True, blank=True)
    observaciones = models.TextField(null=True, blank=True)
    """ Aquí termina"""
    prefijo = models.ForeignKey(Prefijo, on_delete=models.CASCADE)
    servicio = models.CharField(max_length=20)
    modelo = models.ForeignKey(Modelo, on_delete=models.CASCADE)
    tecnologia = models.ForeignKey(Tecnologia, on_delete=models.CASCADE)
    defecto = models.ManyToManyField(Defecto)
    serie = models.CharField(max_length=80)
    nombre_cliente_entrega = models.CharField(max_length=120)
    direccion_cliente_entrega = models.CharField(max_length=120)
    ci_cliente_entrega = models.CharField(max_length=20)
    contacto_telefono = models.CharField(max_length=20)
    propietario = models.BooleanField(default=False)
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE)
    confComercial = models.BooleanField(default=False)
    confTaller = models.BooleanField(default=False)
    entrega = models.ForeignKey(
        Trabajador,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="entrega",
    )

    """ Datos a llenar al reparar"""
    fecha_defectacion = models.DateTimeField(blank=True, null=True)
    repara = models.ForeignKey(
        Trabajador,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="repara",
    )
    accion_reparacion = models.TextField(null=True, blank=True)
    mano_obra = models.ForeignKey(
        ManoObra, on_delete=models.CASCADE, blank=True, null=True
    )
    consumo_recursos = models.ManyToManyField(Consumo_Recursos, blank=True)

    """ Datos antes de cerrada la orden para la gestion de las salidas"""
    fecha_gestion = models.DateTimeField(blank=True, null=True)
    llama = models.ForeignKey(
        Trabajador,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="llama",
    )
    nombre_cliente = models.CharField(max_length=160, blank=True, null=True)
    impresion = models.BooleanField(default=False)

    """ Datos a llenar para cerrar la orden"""
    fecha_cierre = models.DateTimeField(null=True, blank=True)
    cierra = models.ForeignKey(
        Trabajador,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="cierra",
    )
    nombre_cliente_recibe = models.CharField(max_length=120, blank=True, null=True)
    direccion_cliente_recibe = models.CharField(max_length=120, blank=True, null=True)
    ci_cliente_recibe = models.CharField(max_length=20, blank=True, null=True)
    cerrada = models.BooleanField(default=False)

    """ Este dato es muy importante y se actualiza tanto cuando se gestionan los telefonos como cuando cierra"""
    garantia_reparacion = models.DateTimeField(blank=True, null=True)
    """Variable para poder hacer analisis de tiempos"""
    tiempo = models.IntegerField(blank=True, null=True)

    objects = models.Manager()

    def __str__(self):
        return self.No_orden

    # def __str__(self):
    #   return self.No_orden

    class Meta:
        verbose_name_plural = "Ordenes"


class ReporteGestionImpreso(models.Model):
    reporta = models.ForeignKey(Trabajador, on_delete=models.CASCADE)
    ordenes = models.ManyToManyField(OrdenPrimaria)
