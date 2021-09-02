import json
from django.db.models import Q
from django.shortcuts import render
from django.core import serializers
from django.contrib import messages
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.views.generic.list import ListView
from django.utils.translation import gettext_lazy
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

# Models
from api.models import Cliente, Vehiculo, Trabajo, OrdenTrabajo

from admin_taller.forms import ClienteForm, VehiculoForm, TrabajoForm, OrdenTrabajoForm

import logging
from logging.config import fileConfig

# Get an instance of a logger
fileConfig("logging_config.ini")
logger = logging.getLogger(__name__)

# Create your views here.
class InicioTemplateView(TemplateView):
   template_name = 'admin_taller/index.html'

class ClienteList(ListView):
   template_name = 'admin_taller/cliente_list.html'
   model = Cliente
   success_message = "{} {} {}".format(
      gettext_lazy("Lista de "),
      gettext_lazy("Cliente"),
      gettext_lazy("Obtenida")
   )

   def post(self, request, *args, **kwargs):
      if request.is_ajax():
         page_start = request.POST["start"]
         page_len = request.POST["length"]
         draw = request.POST["draw"]
         recordsTotal = 0
         recordsFiltered = 0
         page = int(int(page_start) / int(page_len)) + 1
         columna = request.POST['order[0][column]']
         nombre_columna = request.POST['columns[{}][data]'.format(columna)]
         word_search = request.POST["search[value]"]
         order_by = "id"
         if nombre_columna == "id":
            order_by = "id"
         if nombre_columna == "nombre":
            order_by = "nombre"
         if nombre_columna == "apellido":
            order_by = "apellido"
         if nombre_columna == "telefono":
            order_by = "telefono"
         if nombre_columna == "rfc":
            order_by = "rfc"
         if request.POST["order[0][dir]"] == "desc":
            order_by = "-" + order_by
         recordsTotal = Cliente.objects.all().filter().count()
         cliente = Cliente.objects.all().filter(
            Q(nombre__contains = word_search) |
            Q(apellido__contains = word_search) |
            Q(telefono__contains = word_search) |
            Q(rfc__contains = word_search)
         ).order_by(order_by)
         paginator = Paginator(cliente, int(page_len))
         page_cliente = paginator.page(page).object_list
         data = serializers.serialize(
            "json",
            page_cliente,
            use_natural_foreign_keys=True,
         )
         dato = json.dumps({
            "draw": draw,
            "recordsTotal": recordsTotal,
            "recordsFiltered": paginator.count,
            "data": json.loads(data),
         })
         logger.info('{} {}'.format(self.success_message + ' por', self.request.user))
         return HttpResponse(dato, content_type="application/json")

class ClienteCreate(CreateView):
   template_name = 'admin_taller/cliente_form.html'
   model = Cliente
   form_class = ClienteForm
   success_message = "{} {}".format(
      gettext_lazy("Cliente • "),
      gettext_lazy("Creado exitosamente")
   )
   # success_message = "Save"

   def get_success_url(self, **kwargs):
      context = super().get_context_data(**kwargs)
      dato = context["object"]
      messages.success(self.request, self.success_message)
      logger.info('{} {}'.format(self.success_message + " con el ID: " + str(dato.id) + ' por', self.request.user))
      return reverse_lazy("admin_taller:cliente-list")

class ClienteUpdate(UpdateView):
   template_name = 'admin_taller/cliente_form.html'
   model = Cliente
   form_class = ClienteForm
   success_message = "{} {}".format(
      gettext_lazy("Cliente • "),
      gettext_lazy("Actualizado exitosamente")
   )

   def get_success_url(self, **kwargs):
      context = super().get_context_data(**kwargs)
      dato = context["object"]
      messages.success(self.request, self.success_message)
      logger.info('{} {}'.format(self.success_message + " con el ID: " + str(dato.id) + ' por', self.request.user))
      return reverse_lazy("admin_taller:cliente-list")

class ClienteDelete(DeleteView):
   model = Cliente
   success_message = "{} {}".format(
      gettext_lazy("Cliente • "),
      gettext_lazy("Eliminado exitosamente")
   )

   # for request delete via ajax
   def post(self, request, *args, **kwargs):
      try:
         if request.is_ajax():
            self.object = self.get_object()
            objeto_id = self.object.id
            self.object.delete()
            dato = json.dumps({
               "message": "{} {}".format(
                  gettext_lazy("Cliente • "),
                  gettext_lazy("Eliminado exitosamente")
               )
            })
            logger.info('{} {}'.format(self.success_message + " con el ID: " + str(objeto_id) + ' por', self.request.user))
            return HttpResponse(dato, content_type="application/json")
      except Exception as e:
         if e.__class__.__name__ == "ProtectedError":
            dato = json.dumps({
               "message": "No se puede eliminar, debido a que el cliente tiene beneficiarios asignados."
            })
            return HttpResponse(dato, content_type="application/json")

class VehiculoList(ListView):
   template_name = 'admin_taller/vehiculo_list.html'
   model = Vehiculo
   success_message = "{} {} {}".format(
      gettext_lazy("Lista de "),
      gettext_lazy("Vehiculo"),
      gettext_lazy("Obtenida")
   )

   def post(self, request, *args, **kwargs):
      if request.is_ajax():
         page_start = request.POST["start"]
         page_len = request.POST["length"]
         draw = request.POST["draw"]
         recordsTotal = 0
         recordsFiltered = 0
         page = int(int(page_start) / int(page_len)) + 1
         columna = request.POST['order[0][column]']
         nombre_columna = request.POST['columns[{}][data]'.format(columna)]
         word_search = request.POST["search[value]"]
         order_by = "id"
         if nombre_columna == "id":
            order_by = "id"
         if nombre_columna == "cliente":
            order_by = "cliente"
         if nombre_columna == "tipo":
            order_by = "tipo"
         if nombre_columna == "nombre":
            order_by = "nombre"
         if nombre_columna == "descripcion":
            order_by = "descripcion"
         if nombre_columna == "placa":
            order_by = "placa"
         if nombre_columna == "marca":
            order_by = "marca"
         if nombre_columna == "modelo":
            order_by = "modelo"
         if nombre_columna == "anio":
            order_by = "anio"
         if request.POST["order[0][dir]"] == "desc":
            order_by = "-" + order_by
         recordsTotal = Vehiculo.objects.all().filter().count()
         vehiculo = Vehiculo.objects.all().filter(
            Q(cliente__nombre__contains = word_search) |
            Q(tipo__contains = word_search) |
            Q(nombre__contains = word_search) |
            Q(descripcion__contains = word_search) |
            Q(placa__contains = word_search) |
            Q(marca__contains = word_search) |
            Q(modelo__contains = word_search) |
            Q(anio__contains = word_search)
         ).order_by(order_by)
         paginator = Paginator(vehiculo, int(page_len))
         page_vehiculo = paginator.page(page).object_list
         data = serializers.serialize(
            "json",
            page_vehiculo,
            use_natural_foreign_keys=True,
         )
         dato = json.dumps({
            "draw": draw,
            "recordsTotal": recordsTotal,
            "recordsFiltered": paginator.count,
            "data": json.loads(data),
         })
         logger.info('{} {}'.format(self.success_message + ' por', self.request.user))
         return HttpResponse(dato, content_type="application/json")

class VehiculoCreate(CreateView):
   template_name = 'admin_taller/vehiculo_form.html'
   model = Vehiculo
   form_class = VehiculoForm
   success_message = "{} {}".format(
      gettext_lazy("Vehiculo • "),
      gettext_lazy("Creado exitosamente")
   )
   # success_message = "Save"

   def get_success_url(self, **kwargs):
      context = super().get_context_data(**kwargs)
      dato = context["object"]
      messages.success(self.request, self.success_message)
      logger.info('{} {}'.format(self.success_message + " con el ID: " + str(dato.id) + ' por', self.request.user))
      return reverse_lazy("admin_taller:vehiculo-list")

class VehiculoUpdate(UpdateView):
   template_name = 'admin_taller/vehiculo_form.html'
   model = Vehiculo
   form_class = VehiculoForm
   success_message = "{} {}".format(
      gettext_lazy("Vehiculo • "),
      gettext_lazy("Actualizado exitosamente")
   )

   def get_success_url(self, **kwargs):
      context = super().get_context_data(**kwargs)
      dato = context["object"]
      messages.success(self.request, self.success_message)
      logger.info('{} {}'.format(self.success_message + " con el ID: " + str(dato.id) + ' por', self.request.user))
      return reverse_lazy("admin_taller:vehiculo-list")

class VehiculoDelete(DeleteView):
   model = Vehiculo
   success_message = "{} {}".format(
      gettext_lazy("Vehiculo • "),
      gettext_lazy("Eliminado exitosamente")
   )

   # for request delete via ajax
   def post(self, request, *args, **kwargs):
      try:
         if request.is_ajax():
            self.object = self.get_object()
            objeto_id = self.object.id
            self.object.delete()
            dato = json.dumps({
               "message": "{} {}".format(
                  gettext_lazy("Vehiculo • "),
                  gettext_lazy("Eliminado exitosamente")
               )
            })
            logger.info('{} {}'.format(self.success_message + " con el ID: " + str(objeto_id) + ' por', self.request.user))
            return HttpResponse(dato, content_type="application/json")
      except Exception as e:
         if e.__class__.__name__ == "ProtectedError":
            dato = json.dumps({
               "message": "No se puede eliminar, debido a que el Vehiculo tiene beneficiarios asignados."
            })
            return HttpResponse(dato, content_type="application/json")

class TrabajoList(ListView):
   template_name = 'admin_taller/trabajo_list.html'
   model = Trabajo
   success_message = "{} {} {}".format(
      gettext_lazy("Lista de "),
      gettext_lazy("Trabajo"),
      gettext_lazy("Obtenida")
   )

   def post(self, request, *args, **kwargs):
      if request.is_ajax():
         page_start = request.POST["start"]
         page_len = request.POST["length"]
         draw = request.POST["draw"]
         recordsTotal = 0
         recordsFiltered = 0
         page = int(int(page_start) / int(page_len)) + 1
         columna = request.POST['order[0][column]']
         nombre_columna = request.POST['columns[{}][data]'.format(columna)]
         word_search = request.POST["search[value]"]
         order_by = "id"
         if nombre_columna == "id":
            order_by = "id"
         if nombre_columna == "nombre":
            order_by = "nombre"
         if nombre_columna == "descripcion":
            order_by = "descripcion"
         if nombre_columna == "cantidad":
            order_by = "cantidad"
         if nombre_columna == "precio":
            order_by = "precio"
         if request.POST["order[0][dir]"] == "desc":
            order_by = "-" + order_by
         recordsTotal = Trabajo.objects.all().filter().count()
         trabajo = Trabajo.objects.all().filter(
            Q(nombre__contains = word_search) |
            Q(descripcion__contains = word_search) |
            Q(cantidad__contains = word_search) |
            Q(precio__contains = word_search)
         ).order_by(order_by)
         paginator = Paginator(trabajo, int(page_len))
         page_trabajo = paginator.page(page).object_list
         data = serializers.serialize(
            "json",
            page_trabajo,
            use_natural_foreign_keys=True,
         )
         dato = json.dumps({
            "draw": draw,
            "recordsTotal": recordsTotal,
            "recordsFiltered": paginator.count,
            "data": json.loads(data),
         })
         logger.info('{} {}'.format(self.success_message + ' por', self.request.user))
         return HttpResponse(dato, content_type="application/json")

class TrabajoCreate(CreateView):
   template_name = 'admin_taller/trabajo_form.html'
   model = Trabajo
   form_class = TrabajoForm
   success_message = "{} {}".format(
      gettext_lazy("Trabajo • "),
      gettext_lazy("Creado exitosamente")
   )
   # success_message = "Save"

   def get_success_url(self, **kwargs):
      context = super().get_context_data(**kwargs)
      dato = context["object"]
      messages.success(self.request, self.success_message)
      logger.info('{} {}'.format(self.success_message + " con el ID: " + str(dato.id) + ' por', self.request.user))
      return reverse_lazy("admin_taller:trabajo-list")

class TrabajoUpdate(UpdateView):
   template_name = 'admin_taller/trabajo_form.html'
   model = Trabajo
   form_class = TrabajoForm
   success_message = "{} {}".format(
      gettext_lazy("Trabajo • "),
      gettext_lazy("Actualizado exitosamente")
   )

   def get_success_url(self, **kwargs):
      context = super().get_context_data(**kwargs)
      dato = context["object"]
      messages.success(self.request, self.success_message)
      logger.info('{} {}'.format(self.success_message + " con el ID: " + str(dato.id) + ' por', self.request.user))
      return reverse_lazy("admin_taller:trabajo-list")

class TrabajoDelete(DeleteView):
   model = Trabajo
   success_message = "{} {}".format(
      gettext_lazy("Trabajo • "),
      gettext_lazy("Eliminado exitosamente")
   )

   # for request delete via ajax
   def post(self, request, *args, **kwargs):
      try:
         if request.is_ajax():
            self.object = self.get_object()
            objeto_id = self.object.id
            self.object.delete()
            dato = json.dumps({
               "message": "{} {}".format(
                  gettext_lazy("Trabajo • "),
                  gettext_lazy("Eliminado exitosamente")
               )
            })
            logger.info('{} {}'.format(self.success_message + " con el ID: " + str(objeto_id) + ' por', self.request.user))
            return HttpResponse(dato, content_type="application/json")
      except Exception as e:
         if e.__class__.__name__ == "ProtectedError":
            dato = json.dumps({
               "message": "No se puede eliminar, debido a que el Trabajo tiene beneficiarios asignados."
            })
            return HttpResponse(dato, content_type="application/json")

class OrdenTrabajoList(ListView):
   template_name = 'admin_taller/ordentrabajo_list.html'
   model = OrdenTrabajo
   success_message = "{} {} {}".format(
      gettext_lazy("Lista de "),
      gettext_lazy("OrdenTrabajo"),
      gettext_lazy("Obtenida")
   )

   def post(self, request, *args, **kwargs):
      if request.is_ajax():
         page_start = request.POST["start"]
         page_len = request.POST["length"]
         draw = request.POST["draw"]
         recordsTotal = 0
         recordsFiltered = 0
         page = int(int(page_start) / int(page_len)) + 1
         columna = request.POST['order[0][column]']
         nombre_columna = request.POST['columns[{}][data]'.format(columna)]
         word_search = request.POST["search[value]"]
         order_by = "id"
         if nombre_columna == "id":
            order_by = "id"
         if nombre_columna == "cliente":
            order_by = "cliente"
         if nombre_columna == "vehiculo":
            order_by = "vehiculo"
         if nombre_columna == "numero":
            order_by = "numero"
         if nombre_columna == "fecha_creacion":
            order_by = "fecha_creacion"
         if nombre_columna == "estado":
            order_by = "estado"
         if nombre_columna == "trabajo":
            order_by = "trabajo"
         if nombre_columna == "total":
            order_by = "total"
         if request.POST["order[0][dir]"] == "desc":
            order_by = "-" + order_by
         recordsTotal = OrdenTrabajo.objects.all().filter().count()
         ordentrabajo = OrdenTrabajo.objects.all().filter(
            
            Q(numero__contains = word_search) |
            Q(fecha_creacion__contains = word_search) |
            Q(estado__contains = word_search) |
            # Q(trabajo__contains = word_search) |
            Q(total__contains = word_search)
         ).order_by(order_by)
         paginator = Paginator(ordentrabajo, int(page_len))
         page_ordentrabajo = paginator.page(page).object_list
         data = serializers.serialize(
            "json",
            page_ordentrabajo,
            use_natural_foreign_keys=True,
         )
         dato = json.dumps({
            "draw": draw,
            "recordsTotal": recordsTotal,
            "recordsFiltered": paginator.count,
            "data": json.loads(data),
         })
         logger.info('{} {}'.format(self.success_message + ' por', self.request.user))
         return HttpResponse(dato, content_type="application/json")

class OrdenTrabajoCreate(CreateView):
   template_name = 'admin_taller/ordentrabajo_form.html'
   model = OrdenTrabajo
   form_class = OrdenTrabajoForm
   success_message = "{} {}".format(
      gettext_lazy("OrdenTrabajo • "),
      gettext_lazy("Creado exitosamente")
   )
   # success_message = "Save"

   def get_success_url(self, **kwargs):
      context = super().get_context_data(**kwargs)
      dato = context["object"]
      messages.success(self.request, self.success_message)
      logger.info('{} {}'.format(self.success_message + " con el ID: " + str(dato.id) + ' por', self.request.user))
      return reverse_lazy("admin_taller:ordentrabajo-list")

class OrdenTrabajoUpdate(UpdateView):
   template_name = 'admin_taller/ordentrabajo_form.html'
   model = OrdenTrabajo
   form_class = OrdenTrabajoForm
   success_message = "{} {}".format(
      gettext_lazy("OrdenTrabajo • "),
      gettext_lazy("Actualizado exitosamente")
   )

   def get_success_url(self, **kwargs):
      context = super().get_context_data(**kwargs)
      dato = context["object"]
      messages.success(self.request, self.success_message)
      logger.info('{} {}'.format(self.success_message + " con el ID: " + str(dato.id) + ' por', self.request.user))
      return reverse_lazy("admin_taller:ordentrabajo-list")

class OrdenTrabajoDelete(DeleteView):
   model = OrdenTrabajo
   success_message = "{} {}".format(
      gettext_lazy("OrdenTrabajo • "),
      gettext_lazy("Eliminado exitosamente")
   )

   # for request delete via ajax
   def post(self, request, *args, **kwargs):
      try:
         if request.is_ajax():
            self.object = self.get_object()
            objeto_id = self.object.id
            self.object.delete()
            dato = json.dumps({
               "message": "{} {}".format(
                  gettext_lazy("Orden de Trabajo • "),
                  gettext_lazy("Eliminado exitosamente")
               )
            })
            logger.info('{} {}'.format(self.success_message + " con el ID: " + str(objeto_id) + ' por', self.request.user))
            return HttpResponse(dato, content_type="application/json")
      except Exception as e:
         if e.__class__.__name__ == "ProtectedError":
            dato = json.dumps({
               "message": "No se puede eliminar, debido a que el OrdenTrabajo tiene beneficiarios asignados."
            })
            return HttpResponse(dato, content_type="application/json")