# serializers.py

from rest_framework import serializers

from django.contrib.auth.hashers import make_password
from .models import User, producto_maquina, Producto

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'nombre', 'username','no_empleado','apellido_paterno','apellido_materno', 'rol', 'password', 'is_active', 'is_staff']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)
    
class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto  
        fields = ['id', 'producto', 'descripcion', 'codigo_cliente', 'resina_1', 'categoria', 'estado']
