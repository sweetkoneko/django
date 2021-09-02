from django.urls import path
from django.contrib.auth.decorators import login_required
from admin_taller import views

app_name = 'admin_taller'

urlpatterns = [
   path('', login_required(views.InicioTemplateView.as_view()), name='inicio'),
   # Cliente
   path('cliente/list/', login_required(views.ClienteList.as_view()), name='cliente-list'),
   path('cliente/create/', login_required(views.ClienteCreate.as_view()), name='cliente-create'),
   path('cliente/<int:pk>/delete/', login_required(views.ClienteDelete.as_view()), name='cliente-delete'),
   path('cliente/<int:pk>/update/', login_required(views.ClienteUpdate.as_view()), name='cliente-update'),
   # Vehículo
   path('vehiculo/list/', login_required(views.VehiculoList.as_view()), name='vehiculo-list'),
   path('vehiculo/create/', login_required(views.VehiculoCreate.as_view()), name='vehiculo-create'),
   path('vehiculo/<int:pk>/delete/', login_required(views.VehiculoDelete.as_view()), name='vehiculo-delete'),
   path('vehiculo/<int:pk>/update/', login_required(views.VehiculoUpdate.as_view()), name='vehiculo-update'),
   # Trabajo
   path('trabajo/list/', login_required(views.TrabajoList.as_view()), name='trabajo-list'),
   path('trabajo/create/', login_required(views.TrabajoCreate.as_view()), name='trabajo-create'),
   path('trabajo/<int:pk>/delete/', login_required(views.TrabajoDelete.as_view()), name='trabajo-delete'),
   path('trabajo/<int:pk>/update/', login_required(views.TrabajoUpdate.as_view()), name='trabajo-update'),
   # Orden de Trabajo
   path('ordentrabajo/list/', login_required(views.OrdenTrabajoList.as_view()), name='ordentrabajo-list'),
   path('ordentrabajo/create/', login_required(views.OrdenTrabajoCreate.as_view()), name='ordentrabajo-create'),
   path('ordentrabajo/<int:pk>/delete/', login_required(views.OrdenTrabajoDelete.as_view()), name='ordentrabajo-delete'),
   path('ordentrabajo/<int:pk>/update/', login_required(views.OrdenTrabajoUpdate.as_view()), name='ordentrabajo-update')
]