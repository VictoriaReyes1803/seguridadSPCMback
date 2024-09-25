from django.db import models
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager



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
    user = models.CharField(max_length=100)
    no_empleado = models.CharField(max_length=10)
    nombre = models.CharField(max_length=100)
    apellido_paterno = models.CharField(max_length=100)
    apellido_materno = models.CharField(max_length=100)
    rol = models.CharField(max_length=10, choices=roles)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['no_empleado', 'nombre', 'apellido_paterno', 'apellido_materno', 'rol']

    def __str__(self):
        return self.email + " - " + self.rol

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

class Reporte(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ruta = models.CharField(max_length=150)
    content = models.JSONField()  
    fecha = models.DateTimeField(auto_now_add=True)

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
    nombre = models.CharField(max_length=100)
    codigo = models.CharField(max_length=10)
    estado = models.BooleanField(default=True)
    
    def __str__(self):
        return self.codigo
    
class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    codigo = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    descripcion = models.TextField(max_length=150)
    categoria = models.CharField(max_length=100)
    resina_1 = models.CharField(max_length=100)
    resina_2 = models.CharField(max_length=100)
    estado = models.BooleanField(default=True)
    Maquina = models.ForeignKey(Maquina, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.nombre

class producto_maquina(models.Model):
    Ruta = models.CharField(max_length=100)
    Descripcion_1 = models.CharField(max_length=100)
    Categoria = models.CharField(max_length=100)
    Operación = models.CharField(max_length=100)
    Subcontratacion = models.CharField(max_length=100)
    Centro_trabajo_ppal = models.CharField(max_length=100)
    Destino_ope = models.CharField(max_length=100)
    Cod_maquina = models.ForeignKey(Maquina, on_delete=models.CASCADE)
    Tipo_tpo_operacional = models.CharField(max_length=100)
    Tiempo_ajuste = models.CharField(max_length=100)
    Tpo_operacional = models.CharField(max_length=100)
    Cadencia = models.CharField(max_length=100)
    Cadence_theo = models.CharField(max_length=100)
    Utillaje = models.CharField(max_length=100)
    Eficiencia = models.CharField(max_length=100)
    
    
    def __str__(self):
        return self.Ruta