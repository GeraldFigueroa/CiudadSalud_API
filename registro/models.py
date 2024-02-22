from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

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

    class Meta:
        db_table = 'Persona'


class CustomUserManager(BaseUserManager):
    def create_user(self, identidad, username=None, password=None, **extra_fields):
        if not identidad:
            raise ValueError('El campo identidad debe ser proporcionado')
        if not username:
            username = identidad
        user = self.model(identidad=identidad, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, identidad, username=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Los superusuarios deben tener is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Los superusuarios deben tener is_superuser=True.')
        persona = Persona.objects.get(identidad = identidad)
        return self.create_user(persona, username, password, **extra_fields)

class Usuario(AbstractUser):
    identidad = models.OneToOneField(Persona, on_delete=models.CASCADE, to_field='identidad')
    password = models.CharField(max_length=255)
    es_empleado = models.BooleanField(default=False)
    es_paciente = models.BooleanField(default=False)

    USERNAME_FIELD = 'identidad'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()


    class Meta:
        db_table = 'Usuario'
