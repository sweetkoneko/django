from django.db import models
from django.utils.translation import gettext_lazy

# Create your models here.
class Cliente(models.Model):
   nombre = models.CharField(max_length = 300, blank = False)
   apellido = models.CharField(max_length = 300, blank = False)
   telefono = models.CharField(max_length = 20)
   rfc = models.CharField(max_length = 20)
   fecha_creacion = models.DateTimeField(auto_now = True)

   def natural_key(self):
      return '{} {}'.format(self.nombre, self.apellido)

   def __str__(self):
      return '{} {}'.format(self.nombre, self.apellido)

class Vehiculo(models.Model):
   cliente = models.ForeignKey(
      Cliente,
      verbose_name = gettext_lazy("Propietario"),
      on_delete = models.PROTECT
   )
   tipo = models.CharField(max_length = 100)
   nombre = models.CharField(max_length = 300)
   placa = models.CharField(max_length = 50)
   marca = models.CharField(max_length = 100)
   modelo = models.CharField(max_length = 50)
   anio = models.CharField(
      verbose_name = gettext_lazy("Año"),
      max_length = 20
   )
   descripcion = models.TextField(
      verbose_name = gettext_lazy("Descripción"), help_text = gettext_lazy("Ingrese descripción")
   )

   def natural_key(self):
      return '{}'.format(self.nombre)

   def __str__(self):
      return self.nombre

class Trabajo(models.Model):
   nombre = models.CharField(max_length = 300)
   cantidad = models.IntegerField(null = False, blank = False)
   precio = models.IntegerField(null = False, blank = False)
   descripcion = models.TextField(
      verbose_name = gettext_lazy("Descripción"), help_text = gettext_lazy("Ingrese descripción")
   )

   def natural_key(self):
      return '{}'.format(self.nombre)

   def __str__(self):
      return self.nombre

class OrdenTrabajo(models.Model):
   cliente = models.ForeignKey(
      Cliente,
      verbose_name = gettext_lazy("Cliente"),
      on_delete = models.PROTECT
   )
   vehiculo = models.ForeignKey(
      Vehiculo,
      verbose_name = gettext_lazy("Vehículo"),
      on_delete = models.PROTECT
   )
   numero = models.CharField(max_length = 100)
   fecha_creacion = models.DateTimeField(auto_now = True)
   estado = models.CharField(max_length = 32)
   trabajo = models.ForeignKey(
      Trabajo,
      verbose_name = gettext_lazy("Trabajo"),
      on_delete = models.PROTECT
   )
   total = models.IntegerField(null = False, blank = False)

   def natural_key(self):
      return '{}-{}'.format(self.numero, self.trabajo.nombre)

   def __str__(self):
      return '{}-{}'.format(self.numero, self.trabajo.nombre)