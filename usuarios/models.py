from django.db import models
from django.contrib.auth.models import User

class Trabajador(models.Model):

    ROLES = [
        ('ADMIN', 'Administrador'),
        ('EMPLEADO', 'Empleado'),
    ]

    usuario = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='trabajador',
        null=True,
        blank=True
    )

    dni = models.CharField(max_length=8, unique=True)
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    correo = models.EmailField(unique=True)
    cargo = models.CharField(max_length=100)
    area = models.CharField(max_length=100)
    rol = models.CharField(
        max_length=20,
        choices=ROLES,
        default='EMPLEADO'
    )
    # ALMACENA LA IMAGEN BASE64 DIRECTAMENTE EN POSTGRESQL (Sin usar la carpeta media)
    foto = models.TextField(null=True, blank=True)
    activo = models.BooleanField(default=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"