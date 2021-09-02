from django.shortcuts import render, redirect

# Create your views here.
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth import login, authenticate
from django.http import HttpResponse, HttpResponseRedirect

import json
from django.db.models import Q
from django.core import serializers
from django.core.paginator import Paginator
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.utils.translation import gettext_lazy

from accounts.models import Profile, UserAccount, Profile
from accounts.forms import RegisterForm, ProfileForm, PermissionForm

import os
from django.conf import settings
from django.contrib.auth.models import Permission, User
from django.contrib.contenttypes.models import ContentType

class RegisterView(CreateView):
   model = UserAccount
   form_class = RegisterForm
   template_name = 'accounts/register.html'
   success_message = gettext_lazy("Usuario registrado correctamente")

   def post(self, request, *args, **kwargs):
      form = self.form_class(request.POST)
      if form.is_valid():
         new_user = form.save()
         #because changed username for email in authentication
         username = form.cleaned_data.get('email')
         password = form.cleaned_data.get('password1')
         user = authenticate(username = username, password = password)
         if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse_lazy('viewer:dashboard'))
         else:
            return render(request, self.template_name, {'form': form})

### User Profile ###
class ProfileList(ListView):
   model = Profile
   success_message = '{} {} {}'.format(
      gettext_lazy('Lista de'), 
      gettext_lazy('Usuarios'),
      gettext_lazy('Obtenida')
   )

   def post(self, request, *args, **kwargs):
      if request.is_ajax():
         page_start = request.POST['start']
         page_len = request.POST['length']
         draw = request.POST['draw']
         recordsTotal = 0
         recordsFiltered = 0
         page = int(int(page_start)/int(page_len)) + 1
         word_search = request.POST['search[value]']
         order_by = '-id'
         if request.POST['order[0][column]'] == '1':
            order_by = 'id'
         if request.POST['order[0][column]'] == '2':
            order_by = 'user__first_name'
         if request.POST['order[0][column]'] == '3':
            order_by = 'user__middle_name'
         if request.POST['order[0][column]'] == '4':
            order_by = 'user__last_name'
         if request.POST['order[0][column]'] == '5':
            order_by = 'user__email'
         if request.POST['order[0][column]'] == '6':
            order_by = 'mobile_phone__contains'
         if request.POST['order[0][dir]'] == 'desc':
            order_by = '-' + order_by

         recordsTotal = Profile.objects.all().filter().count()
         users = Profile.objects.all().filter(
            Q(user__first_name__contains = word_search) |
            Q(user__last_name__contains = word_search) |
            Q(user__email__contains = word_search) |
            Q(mobile_phone__contains = word_search)
         ).order_by(order_by)
         paginator = Paginator(users, int(page_len))
         page_users = paginator.page(page).object_list
         data = serializers.serialize('json', page_users, use_natural_foreign_keys=True, )
         dato = json.dumps({
            "draw": draw,
            "recordsTotal": recordsTotal,
            "recordsFiltered": paginator.count,
            "data": json.loads(data)
         })

         return HttpResponse(dato, content_type='application/json')

class ProfileCreate(CreateView):
   model = Profile
   form_class = RegisterForm
   success_message = "{} {}".format(gettext_lazy("Usuario"), gettext_lazy("Creado con Éxito"))

   def get_context_data(self, **kwargs):
      context = super(ProfileCreate, self).get_context_data(**kwargs)
      context["grupos"] = self.request.user.groups.all()
      return context

   def get_success_url(self, **kwargs):
      context = super().get_context_data(**kwargs)
      user = context['object']
      messages.success(self.request, self.success_message)
      return reverse_lazy('accounts:update',  kwargs = {'pk': user.id})

   def get_form_kwargs(self, **kwargs):
      form_kwargs = super(ProfileCreate, self).get_form_kwargs(**kwargs)
      form_kwargs["usuario"] = self.request.user
      return form_kwargs

class ProfileUpdate(UpdateView):
   model = Profile
   form_class = ProfileForm
   success_message = "{} {}".format(gettext_lazy("Usario"), gettext_lazy("Actualizado Exitosamente"))

   def get_context_data(self, **kwargs):
      context = super(ProfileUpdate, self).get_context_data(**kwargs)
      context["grupos"] = self.request.user.groups.all()
      return context

   def get_success_url(self, **kwargs):
      context = super().get_context_data(**kwargs)
      user = context['object']
      messages.success(self.request, self.success_message)
      return reverse_lazy('accounts:update',  kwargs = {'pk': user.id})

   def get_form_kwargs(self, **kwargs):
      form_kwargs = super(ProfileUpdate, self).get_form_kwargs(**kwargs)
      form_kwargs["usuario"] = self.request.user
      return form_kwargs

   def form_valid(self, form):
      if ((self.object.pk == self.request.user.id) or
         (self.request.user.is_superuser) or
         ( 'ADMIN' in [ g.name for g in self.request.user.groups.all()] )
      ):
         self.object = form.save()
         return super().form_valid(form)
      else:
         return super().form_invalid(form)

class ProfileDelete(DeleteView):
   model = Profile
   success_message = "{} {}".format(gettext_lazy("Usuario"), gettext_lazy("Eliminado Exitosamente"))

   #for request delete via ajax
   def post(self, request, *args, **kwargs):
      if request.is_ajax():
         self.object = self.get_object()
         self.object.delete()
         dato = json.dumps({
            "message": "{} {}".format(gettext_lazy("Usuario"), gettext_lazy("Eliminado Exitosamente"))
         })
         return HttpResponse(dato, content_type="application/json")