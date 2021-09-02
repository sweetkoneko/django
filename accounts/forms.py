from django.forms import ModelForm
from django.forms import CharField, ModelMultipleChoiceField
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.utils.translation import gettext_lazy
from django.utils.translation import ugettext, ugettext_lazy as _
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate

from accounts.models import Profile, UserAccount
from django.contrib.auth.models import Group, Permission
from django import forms
# from authy.api import AuthyApiClient
from django.conf import settings

class RegisterForm(UserCreationForm):
    password1 = forms.CharField(
       widget=forms.PasswordInput,
       help_text=gettext_lazy("Ingresa tu contraseña"),
       label=gettext_lazy('Contraseña'),
    )
    def __init__(self, usuario, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)

        ## add attributes
        for name, field in self.fields.items():
            field.widget.attrs['placeholder'] = field.help_text
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = get_user_model()
        custom_fields = ('first_name', 'middle_name', 'last_name', 'email', 'groups' )
        fields = UserCreationForm.Meta.fields + custom_fields

    def save(self, *args, **kwargs):
        super(RegisterForm, self).save(*args, **kwargs)
        self.instance.groups.set(self.cleaned_data.get('groups'))
        self.instance.save()
        return self.instance

class ProfileForm(ModelForm):
    # fields of UserAccounts
    first_name = CharField(
       label=gettext_lazy('Nombre'), help_text=gettext_lazy("Ingrese su nombre"))
    middle_name = CharField(label=gettext_lazy('Apellido Paterno'), help_text=gettext_lazy("Ingrese su apellido"))
    last_name = CharField(label=gettext_lazy('Apellido Materno'), help_text=gettext_lazy("Ingrese su apellido"))
    email = CharField(label=gettext_lazy('Correo'),)
    username = CharField(label=gettext_lazy('Nombre de usuario') )

    def __init__(self, usuario, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].initial = self.instance.user.first_name
        self.fields['middle_name'].initial = self.instance.user.middle_name
        self.fields['last_name'].initial = self.instance.user.last_name
        self.fields['email'].initial = self.instance.user.email
        self.fields['username'].initial = self.instance.user.username
        self.usuario = usuario

        ## add attributes
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['email'].widget.attrs['readonly'] = True
            self.fields['email'].widget.attrs['style'] = 'background-color: #e3e6ec;'
            self.fields['username'].widget.attrs['readonly'] = True
            self.fields['username'].widget.attrs['style'] = 'background-color: #e3e6ec;'

        # check this - redundant
        for name, field in self.fields.items():
            field.widget.attrs['placeholder'] = field.help_text
            field.widget.attrs['class'] = 'form-control'

    def save(self, *args, **kwargs):
        super(ProfileForm, self).save(*args, **kwargs)
        self.instance.user.first_name = self.cleaned_data.get('first_name')
        self.instance.user.middle_name = self.cleaned_data.get('middle_name')
        self.instance.user.last_name = self.cleaned_data.get('last_name')
        self.instance.user.save()
        return self.instance

    class Meta:
        model = Profile
        custom_fields = (
           'picture',
           'first_name',
           'middle_name',
           'last_name',
           'email',
           'username',
           'office_phone',
           'mobile_phone',
            'street_address',
            'zipcode_address',
            'city_address',
            'state_address',
            'country_address'
         )
        fields = custom_fields

class PermissionForm(ModelForm):
    # fields of UserAccounts
    user_permissions = ModelMultipleChoiceField(
        required = False,
        queryset = Permission.objects.filter(name__contains = "Access"),
        widget = forms.CheckboxSelectMultiple(),
        label = gettext_lazy('User permissions'),
    )

    def __init__(self, *args, **kwargs):
        super(PermissionForm, self).__init__(*args, **kwargs)
        if self.instance.user.user_permissions.all():
           self.fields['user_permissions'].initial = self.instance.user.user_permissions.all()
        else:
           permisos_grupo = [permiso.replace('admin_unit.', '') for permiso in self.instance.user.get_group_permissions()]
           self.fields['user_permissions'].initial = Permission.objects.filter(codename__in=permisos_grupo)

        self.fields['user_permissions'].label_from_instance = lambda obj: "%s" % _(obj.name)

        # check this - redundant
        for name, field in self.fields.items():
            field.widget.attrs['placeholder'] = field.help_text

    def save(self, *args, **kwargs):
        super(PermissionForm, self).save(*args, **kwargs)
        self.instance.user.user_permissions.set(self.cleaned_data.get('user_permissions'))
        self.instance.user.save()
        return self.instance

    class Meta:
        model = Profile
        custom_fields = ('user_permissions',)
        fields = custom_fields

class ChangePasswordForm(PasswordChangeForm):
   def __init__(self, *args, **kwargs):
      super(ChangePasswordForm, self).__init__(*args, **kwargs)
      for visible in self.visible_fields():
         visible.field.widget.attrs['class'] = 'form-control string'