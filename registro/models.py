from django.db import models
from django.contrib.auth.models import AbstractUser

class Persona(models.Model):
    identidad = models.CharField(max_length=15, primary_key=True)
    email = models.CharField(max_length=255, unique=True)
    primer_nombre = models.CharField(max_length=50, null=False)
    segundo_nombre = models.CharField(max_length=50, default='')
    primer_apellido = models.CharField(max_length=50, null=False)
    segundo_apellido = models.CharField(max_length=50, default='')
    fecha_nacimiento = models.DateField()
    telefono = models.CharField(max_length=9, null=False)
    direccion = models.CharField(max_length=500)
    estado_civil = models.CharField(max_length=100)


class Usuario(AbstractUser):
    identidad = models.OneToOneField(Persona, on_delete=models.CASCADE, to_field='identidad')
    password = models.CharField(max_length=255)
    username = None
    es_empleado = models.BooleanField(default=False)
    es_paciente = models.BooleanField(default=False)

    USERNAME_FIELD = 'identidad'
    REQUIRED_FIELDS = []
