# serializers.py

from rest_framework import serializers

from django.contrib.auth.hashers import make_password
from .models import User, Producto_maquina, Producto, Maquina, Reporte

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','email', 'nombre', 'username','no_empleado','apellido_paterno','apellido_materno', 'rol', 'password', 'is_active', 'is_staff']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)
    
class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto  
        fields = ['id', 'producto', 'descripcion', 'codigo_cliente', 'resina_1', 'categoria', 'estado']
        
class MaquinaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Maquina
        fields = ['id', 'maquina', 'estado']
        
        
class ProductoMaquinaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto_maquina
        fields = ['id', 'Ruta', 'Descripcion_1', 'Categoria', 'Operación', 'Subcontratacion', 'Centro_trabajo_ppal', 'Destino_ope', 'Cod_maquina',
                  'Tipo_tpo_operacional', 'Tiempo_ajuste', 'Tpo_operacional', 'Cadencia',
                  'Cadence_theo', 'Utillaje', 'Eficiencia']
        
class ReporteSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True) 
    producto = ProductoSerializer(read_only=True)
    producto_maquina = ProductoMaquinaSerializer(read_only=True)
    
    producto_id = serializers.PrimaryKeyRelatedField(
        queryset=Producto.objects.all(), write_only=True, source='producto'
    )
    producto_maquina_id = serializers.PrimaryKeyRelatedField(
        queryset=Producto_maquina.objects.all(), write_only=True, source='producto_maquina'
    )
    class Meta:
        model = Reporte
        fields = ['id','user','producto','producto_id', 'producto_maquina','producto_maquina_id','ruta', 'content','fecha','formato']
        read_only_fields = ['fecha', 'user']