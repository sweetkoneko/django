from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view

from api.models import Cliente, Vehiculo, Trabajo, OrdenTrabajo
from api.serializers import ClienteSerializer, VehiculoSerializer, TrabajoSerializer
from api.serializers import OrdenTrabajoSerializer

# Create your views here.

# Forma 1
class ClienteViewset(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer

class VehiculoViewset(viewsets.ModelViewSet):
    queryset = Vehiculo.objects.all()
    serializer_class = VehiculoSerializer

class TrabajoViewset(viewsets.ModelViewSet):
    queryset = Trabajo.objects.all()
    serializer_class = TrabajoSerializer

class OrdenTrabajoViewset(viewsets.ModelViewSet):
    queryset = OrdenTrabajo.objects.all()
    serializer_class = OrdenTrabajoSerializer

# Forma 2
@api_view(['GET', 'POST'])
def cliente_list(request):
    if request.method == 'GET':
        clientes = Cliente.objects.all()
        serializer = ClienteSerializer(clientes, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ClienteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def cliente_detail(request, pk):
    try:
        cliente = Cliente.objects.get(pk=pk)
    except Cliente.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ClienteSerializer(cliente)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ClienteSerializer(cliente, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        cliente.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
def vehiculo_list(request):
    if request.method == 'GET':
        vehiculos = Vehiculo.objects.all()
        serializer = VehiculoSerializer(vehiculos, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = VehiculoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def vehiculo_detail(request, pk):
    try:
        vehiculo = Vehiculo.objects.get(pk=pk)
    except Vehiculo.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = VehiculoSerializer(vehiculo)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = VehiculoSerializer(vehiculo, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        vehiculo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
def trabajo_list(request):
    if request.method == 'GET':
        trabajos = Trabajo.objects.all()
        serializer = TrabajoSerializer(trabajos, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = TrabajoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def trabajo_detail(request, pk):
    try:
        trabajo = Trabajo.objects.get(pk=pk)
    except Trabajo.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = TrabajoSerializer(trabajo)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = TrabajoSerializer(trabajo, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        trabajo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
def ordentrabajo_list(request):
    if request.method == 'GET':
        ordenestrabajo = OrdenTrabajo.objects.all()
        serializer = OrdenTrabajoSerializer(ordenestrabajo, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = OrdenTrabajoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def ordentrabajo_detail(request, pk):
    try:
        ordentrabajo = OrdenTrabajo.objects.get(pk=pk)
    except OrdenTrabajo.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = OrdenTrabajoSerializer(ordentrabajo)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = OrdenTrabajoSerializer(ordentrabajo, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        ordentrabajo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)