from django.contrib import admin

from infracciones.models import (
    Persona,
    Vehiculo,
    Oficial,
)

@admin.register(Persona)
class PersonaAdmin(admin.ModelAdmin):
    list_display = ("nombre",)
    ordering = ["nombre"]
    search_fields = ["nombre"]


@admin.register(Vehiculo)
class VehiculoAdmin(admin.ModelAdmin):
    list_display = ("placa_de_patente",)
    ordering = ["placa_de_patente"]
    search_fields = ["placa_de_patente"]

from django.contrib.auth.admin import UserAdmin
@admin.register(Oficial)
class OficialAdmin(UserAdmin):
    list_display = ("nombre",)
    ordering = ["nombre"]
    search_fields = ["nombre"]
    fieldsets = (
        (None, {'fields': ('numero_unico_identificatorio', 'nombre')}),
    )
    add_fieldsets = (
        (None, {'fields': ('numero_unico_identificatorio', 'nombre', 'password1', 'password2')}),
    )