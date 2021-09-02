from django.db import models

# Create your models here.
import os
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils.translation import gettext_lazy
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import PermissionsMixin

""" from admin_unit.models import AdminUnit """

### - Changing AbstractUser - username for email in authentication - ###
class UserAccount(AbstractUser):
   email = models.EmailField(
      gettext_lazy('Correo'),
      max_length = 255,
      unique = True,
      help_text = gettext_lazy("Introduce tu correo electrónico")
   )
   first_name = models.CharField(
      gettext_lazy('Nombre'),
      help_text = gettext_lazy("Introduce tu nombre"),
      max_length = 150,
      blank = True
   )
   middle_name = models.CharField(
      gettext_lazy('Apellido Paterno'),
      help_text = gettext_lazy("Introduce tu apellido materno"),
      max_length = 150,
      blank = True
   )
   last_name = models.CharField(
      gettext_lazy('Apellido Materno'),
      help_text = gettext_lazy("Introduce tu apellido paterno"),
      max_length = 150,
      blank = True
   )

   USERNAME_FIELD = 'email'
   REQUIRED_FIELDS = ['username']

   def natural_key(self):
      return ({
         'groups': [ g.name for g in self.groups.all() ],
         'first_name':self.first_name,
         'middle_name':self.middle_name,
         'last_name':self.last_name,
         'email':self.email,
         'username':self.username
      })

   def __str__(self):
       return self.email

### - User Profile, Roles, Groups - ###
def upload_to(instance, filename):
   path = instance.user.username + '/files' + '/pictures'
   return '{}/{}'.format(path, filename)

class Profile(models.Model):
   user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete = models.PROTECT,)
   """ admin_unit = models.ForeignKey(AdminUnit, verbose_name=gettext_lazy('Admin Unit'), on_delete=models.PROTECT, blank=True, null=True,) """
   picture = models.ImageField(
      upload_to = upload_to,
      verbose_name = gettext_lazy('Imágen'),
      help_text = gettext_lazy('Imagen de usuario'),
      null = True,
      blank = True
   )
   street_address = models.CharField(
      verbose_name = gettext_lazy('Calle'),
      max_length = 250,
      blank = True,
      help_text = gettext_lazy("Ingrese la calle")
   )
   locality_address = models.CharField(
      verbose_name = gettext_lazy('Localidad / Pueblo / Municipio'),
      max_length = 250,
      blank = True
   )
   zipcode_address = models.CharField(
      verbose_name = gettext_lazy('Código postal'),
      max_length = 10,
      blank = True,
      help_text = gettext_lazy("Ingrese su código postal")
   )
   city_address = models.CharField(
      verbose_name = gettext_lazy('Ciudad'),
      max_length = 100,
      blank = True,
      help_text = gettext_lazy("Ingrese la ciudad")
   )
   state_address = models.CharField(
      verbose_name = gettext_lazy('Estado'),
      max_length = 100,
      blank = True,
      help_text = gettext_lazy("Ingrese su estado")
   )
   country_address = models.CharField(
      verbose_name = gettext_lazy('País'),
      max_length = 100,
      blank = True,
      help_text = gettext_lazy("Ingrese un país")
   )
   office_phone = models.CharField(
      verbose_name = gettext_lazy('Teléfono de oficina'),
      max_length = 20,
      blank = True,
      help_text = gettext_lazy("Ingrese un teléfono")
   )
   mobile_phone = models.CharField(
      verbose_name = gettext_lazy('Teléfono móvil'),
      max_length = 20,
      blank = True,
      help_text = gettext_lazy("Ingrese teléfono móvil")
   )

   def __str__(self):
      return '{} {}'.format(self.user.first_name, self.user.last_name)

@receiver(post_save, sender=UserAccount)
def create_user_profile(sender, instance, created, **kwargs):
   if created:
      #if user created then create profile and make dir for personal files
      Profile.objects.create(user=instance)

      directory = settings.MEDIA_ROOT + '/' + str(instance.username) + '/files'
      if not os.path.exists(directory):
         os.makedirs(directory)

@receiver(post_save, sender=UserAccount)
def save_user_profile(sender, instance, **kwargs):
   instance.profile.save()