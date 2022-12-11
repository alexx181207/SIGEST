from django.db import models
from django.conf import settings


# Create your models here.
class Division_Territorial(models.Model):
    division = models.CharField(max_length=60)

    def __str__(self):
        return self.division


class Prefijo(models.Model):
    nombre = models.CharField(max_length=8, blank=True)

    def __str__(self):
        return self.nombre


class Centro_Telecomunicaciones(models.Model):
    division = models.ForeignKey(Division_Territorial, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=60)

    def __str__(self):
        return self.nombre


class Centro(models.Model):
    centro_telecomunicaciones = models.ForeignKey(
        Centro_Telecomunicaciones, on_delete=models.CASCADE
    )
    nombre = models.CharField(max_length=60)

    def __str__(self):
        return self.nombre


class ManoObra(models.Model):
    tipo = models.CharField(max_length=300)
    codigo_sap = models.CharField(max_length=60)
    precio = models.FloatField()

    def __str__(self):
        return self.tipo


class Estado(models.Model):
    nombre = models.CharField(max_length=60)

    def __str__(self):
        return self.nombre


class Defecto(models.Model):
    nombre = models.CharField(max_length=60)

    def __str__(self):
        return self.nombre


class Tecnologia(models.Model):
    nombre = models.CharField(max_length=40)

    def __str__(self):
        return self.nombre


class Recursos(models.Model):
    descripcion = models.CharField(max_length=80)
    codigo_sap = models.CharField(max_length=60)
    precio = models.FloatField()

    def __str__(self):
        return self.descripcion


class Consumo_Recursos(models.Model):
    recurso = models.ForeignKey(Recursos, on_delete=models.CASCADE)
    centro = models.ForeignKey(Centro, on_delete=models.CASCADE)
    fecha = models.DateTimeField()
    cantidad = models.IntegerField()
    importe = models.FloatField()
    asociado_orden = models.BooleanField(default=False)

    def __str__(self):
        return self.recurso.descripcion


class Modelo(models.Model):
    nombre = models.CharField(max_length=60)
    tecnologia = models.ForeignKey(Tecnologia, on_delete=models.CASCADE)
    codigo_sap = models.CharField(max_length=60)
    descripcion = models.CharField(max_length=160)

    def __str__(self):
        return self.nombre


# class OrdenPendiente(models.Manager):
# def get_queryset(self):
# return super(OrdenPendiente, self).get_queryset().filter(estado=get_object_or_404(Estado, pk=2))


class Especialidad(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Trabajador(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    centro = models.ForeignKey(Centro, on_delete=models.CASCADE)
    codigo_siprec = models.CharField(max_length=30)
    especialidad = models.ForeignKey(Especialidad, on_delete=models.CASCADE)

    def __str__(self):
        return "%s %s" % (self.user.first_name, self.user.last_name)

    class Meta:
        verbose_name_plural = "Trabajadores"


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


class OrdenHistorico(models.Model):
    orden_reparada = models.ForeignKey(OrdenPrimaria, on_delete=models.CASCADE)
    prefijo = models.CharField(max_length=60, null=True, blank=True)
    servicio = models.CharField(max_length=60, null=True, blank=True)
    centro = models.ForeignKey(Centro, on_delete=models.CASCADE)
    fecha_defectacion = models.DateTimeField()
    accion_reparacion = models.TextField()
    estado_defectadas = models.ForeignKey(Estado, on_delete=models.CASCADE)


class ReporteGestionImpreso(models.Model):
    reporta = models.ForeignKey(Trabajador, on_delete=models.CASCADE)
    ordenes = models.ManyToManyField(OrdenPrimaria)
