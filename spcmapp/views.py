
from django.shortcuts import get_object_or_404, render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework import generics
from .models import  Producto, producto_maquina, Maquina
from .serializers import  ProductoSerializer, MaquinaSerializer, ProductoMaquinaSerializer
from rest_framework.response import Response
from rest_framework import status


class Productos(LoginRequiredMixin, generics.ListCreateAPIView):
    serializer_class = ProductoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Producto.objects.filter(estado=True)  
        
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class ProductoMaquina(LoginRequiredMixin, generics.ListCreateAPIView):
    serializer_class = ProductoMaquinaSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, producto , *args, **kwargs):
        producto_maquina_obj = get_object_or_404(producto_maquina, Ruta=producto)

        if producto_maquina_obj:
            serializer = ProductoMaquinaSerializer(producto_maquina_obj)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Producto no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        
class Maquinaget(generics.ListAPIView):
    queryset = Maquina.objects.filter(estado=True)  
    serializer_class = MaquinaSerializer
    permission_classes = [IsAuthenticated]  

    def get(self, request, *args, **kwargs):
        maquinas = self.get_queryset()
        serializer = self.get_serializer(maquinas, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
