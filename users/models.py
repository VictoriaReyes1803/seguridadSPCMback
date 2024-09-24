from django.db import models

from django.db import models

class User(models.Model):
    PERMISSIONS = [
        ('admin', 'Admin'),
        ('engineer', 'Engineer'),
        ('technician', 'Technician'),
    ]
    email = models.EmailField(unique=True)
    nombre = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    permisos = models.CharField(max_length=10, choices=PERMISSIONS)

    def __str__(self):
        return self.email


class Reporte(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ruta = models.CharField(max_length=255)
    content = models.JSONField()  # Guarda el contenido en formato JSON
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reporte {self.id} de {self.user.email}"


class Actividad(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reporte = models.ForeignKey(Reporte, on_delete=models.CASCADE)
    act = models.TextField()

    def __str__(self):
        return f"Actividad {self.id} por {self.user.email}"
