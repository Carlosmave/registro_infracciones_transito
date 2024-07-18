from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from infracciones.managers import CustomUserManager

class Persona(models.Model):
    nombre = models.CharField(
        max_length=200, blank=False, null=False
    )
    email = models.EmailField(_("email address"), unique=True)

    class Meta:
        verbose_name = "Persona"
        verbose_name_plural = "Personas"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre

class Vehiculo(models.Model):
    placa_de_patente = models.CharField(
        max_length=200, blank=False, null=False, unique=True
    )
    marca = models.CharField(
        max_length=200, blank=False, null=False
    )
    color = models.CharField(
        max_length=200, blank=False, null=False
    )
    persona = models.ForeignKey(
        Persona,
        on_delete=models.CASCADE,
        related_name="persona_vehiculos",
        blank=False,
        null=False,
    )

    class Meta:
        verbose_name = "Vehiculo"
        verbose_name_plural = "Vehiculos"
        ordering = ["placa_de_patente"]

    def __str__(self):
        return self.placa_de_patente
    
class Oficial(AbstractUser):
    numero_unico_identificatorio = models.CharField(
        max_length=200, blank=False, null=False, unique=True
    )
    nombre = models.CharField(
        max_length=200, blank=False, null=False
    )
    USERNAME_FIELD = "numero_unico_identificatorio"
    REQUIRED_FIELDS = ["nombre"]
    objects = CustomUserManager()
    username = None

    class Meta:
        verbose_name = "Oficial"
        verbose_name_plural = "Oficiales"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre
    

class Infraccion(models.Model):
    timestamp = models.DateTimeField()
    comentarios = models.CharField(
        max_length=200, blank=False, null=False
    )
    vehiculo = models.ForeignKey(
        Vehiculo,
        on_delete=models.CASCADE,
        related_name="vehiculo_infracciones",
        blank=False,
        null=False,
    )
    oficial = models.ForeignKey(
        Oficial,
        on_delete=models.CASCADE,
        related_name="oficial_infracciones",
        blank=False,
        null=False,
    )

    class Meta:
        verbose_name = "Infraccion"
        verbose_name_plural = "Infracciones"
        ordering = ["vehiculo__placa_de_patente"]

    def __str__(self):
        return self.vehiculo.placa_de_patente