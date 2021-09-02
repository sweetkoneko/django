from rest_framework import serializers
from rest_framework import fields
from .models import Cliente, Vehiculo, Trabajo, OrdenTrabajo


class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'

class VehiculoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehiculo
        fields = '__all__'

class TrabajoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trabajo
        fields = '__all__'

class OrdenTrabajoSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrdenTrabajo
        fields = '__all__'