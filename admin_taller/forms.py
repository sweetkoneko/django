from django.forms import ModelForm
from django import forms
from api.models import Cliente, Vehiculo, Trabajo, OrdenTrabajo

class DateInput(forms.DateInput):
   input_type = "date"

class ClienteForm(ModelForm):
   def __init__(self, *args, **kwargs):
      super(ClienteForm, self).__init__(*args, **kwargs)
      # Add attributes
      for name, field in self.fields.items():
         field.widget.attrs["placeholder"] = field.help_text
         field.widget.attrs["class"] = "form-control"
   
   class Meta:
      model = Cliente
      fields = "__all__"

class VehiculoForm(ModelForm):
   def __init__(self, *args, **kwargs):
      super(VehiculoForm, self).__init__(*args, **kwargs)
      # Add attributes
      for name, field in self.fields.items():
         field.widget.attrs["placeholder"] = field.help_text
         field.widget.attrs["class"] = "form-control"
         if name == "descripcion":
            field.widget.attrs["rows"] = "2"
   
   class Meta:
      model = Vehiculo
      fields = "__all__"

class TrabajoForm(ModelForm):
   def __init__(self, *args, **kwargs):
      super(TrabajoForm, self).__init__(*args, **kwargs)
      # Add attributes
      for name, field in self.fields.items():
         field.widget.attrs["placeholder"] = field.help_text
         field.widget.attrs["class"] = "form-control"
         if name == "descripcion":
            field.widget.attrs["rows"] = "2"
   
   class Meta:
      model = Trabajo
      fields = "__all__"

class OrdenTrabajoForm(ModelForm):
   def __init__(self, *args, **kwargs):
      super(OrdenTrabajoForm, self).__init__(*args, **kwargs)
      # Add attributes
      for name, field in self.fields.items():
         field.widget.attrs["placeholder"] = field.help_text
         field.widget.attrs["class"] = "form-control"
   
   class Meta:
      model = OrdenTrabajo
      fields = "__all__"