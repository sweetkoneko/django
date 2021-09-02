# from django.contrib import admin
from django.urls import path
from rest_framework import routers
from django.urls.conf import include
from api import views

router = routers.DefaultRouter()
router.register('cliente', views.ClienteViewset, basename='cliente')
router.register('vehiculo', views.VehiculoViewset, basename='vehiculo')
router.register('trabajo', views.TrabajoViewset, basename='trabajo')
router.register('ordentrabajo', views.OrdenTrabajoViewset, basename='ordentrabajo')

urlpatterns = [
    path('', include(router.urls)),
    path('clientes/', views.cliente_list),
    path('clientes/<int:pk>', views.cliente_detail),
    path('vehiculos/', views.vehiculo_list),
    path('vehiculos/<int:pk>', views.vehiculo_detail),
    path('trabajos/', views.trabajo_list),
    path('trabajos/<int:pk>', views.trabajo_detail),
    path('ordenestrabajo/', views.ordentrabajo_list),
    path('ordenestrabajo/<int:pk>', views.ordentrabajo_detail),
    
]