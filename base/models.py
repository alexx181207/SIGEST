from django.db import models
from django.conf import settings

# Create your models here.

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


class Modelo(models.Model):
    nombre = models.CharField(max_length=60)
    tecnologia = models.ForeignKey(Tecnologia, on_delete=models.CASCADE)
    codigo_sap = models.CharField(max_length=60)
    descripcion = models.CharField(max_length=160)

    def __str__(self):
        return self.nombre


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

class Consumo_Recursos(models.Model):
    recurso = models.ForeignKey(Recursos, on_delete=models.CASCADE)
    centro = models.ForeignKey(Centro, on_delete=models.CASCADE)
    fecha = models.DateTimeField()
    cantidad = models.IntegerField()
    importe = models.FloatField()
    asociado_orden = models.BooleanField(default=False)

    def __str__(self):
        return self.recurso.descripcion
