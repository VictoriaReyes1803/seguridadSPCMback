from django.db import models
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
import jwt
from django.conf import settings
from django.utils import timezone
from datetime import timedelta


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('El email debe ser proporcionado')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser):
    roles = [
        ('admin', 'Admin'),
        ('engineer', 'Engineer'),
        ('technician', 'Technician'),
    ]
    email = models.EmailField(unique=True, max_length=150)
    username = models.CharField(unique=True, max_length=100)
    no_empleado = models.CharField(max_length=10, null=True, blank=True)
    nombre = models.CharField(max_length=100)
    apellido_paterno = models.CharField(max_length=100)
    apellido_materno = models.CharField(max_length=100, null=True)
    rol = models.CharField(max_length=10, choices=roles)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    code = models.CharField(max_length=100, null=True, blank=True)
    reset_token = models.CharField(max_length=100, null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','no_empleado', 'nombre', 'apellido_paterno', 'apellido_materno', 'rol']

    def __str__(self):
        return self.email + " - " + self.rol
    
    def generate_reset_token(self):
        """Genera un token JWT para restablecimiento de contraseña."""
        expiration = timezone.now() + timedelta(minutes=60)  
        token = jwt.encode({
            'user_id': self.id,
            'exp': int(expiration.timestamp())
        }, settings.SECRET_KEY, algorithm='HS256')
        return token

    def verify_reset_token(self, token):
        """Verifica la validez del token JWT para restablecimiento de contraseña."""
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            
            return payload['user_id'] == self.id  
        except jwt.ExpiredSignatureError:
            return False
        except (jwt.DecodeError, jwt.InvalidTokenError):
            return False
    def set_password(self, raw_password):
        self.password = make_password(raw_password)

class Reporte(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ruta = models.CharField(max_length=150)
    content = models.JSONField()  
    formato = models.CharField(max_length=100)
    fecha = models.DateTimeField(auto_now_add=True)
    producto = models.ForeignKey('Producto', on_delete=models.CASCADE)
    producto_maquina = models.ForeignKey('Producto_maquina', on_delete=models.CASCADE)
    

    def __str__(self):
        return f"Reporte {self.id} de {self.user.email}"


class Actividad(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reporte = models.ForeignKey(Reporte, on_delete=models.CASCADE)
    act = models.TextField()

    def __str__(self):
        return f"Actividad {self.id} por {self.user.email}"

class Cliente(models.Model):
    codigo = models.CharField(max_length=10)
    nombre = models.CharField(max_length=100)
    
    def __str__(self):
        return self.codigo
    
class Maquina(models.Model):
    maquina = models.CharField(max_length=100)
    estado = models.BooleanField(default=True, null=True, blank=True)
    
    def __str__(self):
        return self.codigo
    
class Producto(models.Model):
    
    producto = models.CharField(max_length=100)
    descripcion = models.TextField(max_length=150)
    codigo_cliente = models.CharField(max_length=100)
    resina_1 = models.CharField(max_length=100)
    categoria = models.CharField(max_length=100)
    estado = models.BooleanField(default=True)
    
    resina_2 = models.CharField(max_length=100, null=True, blank=True)
    Maquina = models.CharField(max_length=100, null=True, blank=True)
    
    def __str__(self):
        return self.producto

class Producto_maquina(models.Model):
    Ruta = models.CharField(max_length=100)
    Descripcion_1 = models.CharField(max_length=100)
    Categoria = models.CharField(max_length=100)
    Operación = models.IntegerField()
    Subcontratacion = models.CharField(max_length=100)
    Centro_trabajo_ppal = models.CharField(max_length=100)
    Destino_ope = models.CharField(max_length=100)
    Cod_maquina = models.CharField(max_length=100)
    Tipo_tpo_operacional = models.CharField(max_length=100)
    Tiempo_ajuste = models.FloatField()
    Tpo_operacional = models.FloatField()
    Cadencia = models.FloatField()
    Cadence_theo = models.CharField(max_length=100)
    Utillaje = models.CharField(max_length=100)
    Eficiencia = models.CharField(max_length=100)
    
    
    def __str__(self):
        return self.Ruta
