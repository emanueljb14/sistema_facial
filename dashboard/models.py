from django.db import models

class UsuarioSistema(models.Model):
    ROL_CHOICES = [
        ('ADMIN', 'Administrador'),
        ('OPERADOR', 'Operador'),
        ('EMPLEADO', 'Empleado/Personal'),
    ]

    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    dni = models.CharField(max_length=15, unique=True)
    correo = models.EmailField(unique=True)
    rol = models.CharField(max_length=20, choices=ROL_CHOICES, default='EMPLEADO')
    foto_referencia = models.ImageField(upload_to='rostros/', null=True, blank=True)
    activo = models.BooleanField(default=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.dni})"


class Asistencia(models.Model):
    usuario = models.ForeignKey(UsuarioSistema, on_delete=models.CASCADE, related_name='asistencias')
    fecha_hora = models.DateTimeField(auto_now_add=True)
    tipo = models.CharField(max_length=10, choices=[('ENTRADA', 'Entrada'), ('SALIDA', 'Salida')])
    confianza_ia = models.FloatField(help_text="Porcentaje de similitud detectado por la IA")

    def __str__(self):
        return f"{self.usuario.nombre} - {self.tipo} - {self.fecha_hora.strftime('%Y-%m-%d %H:%M')}"