from django.contrib import admin
from .models import Trabajador


@admin.register(Trabajador)
class TrabajadorAdmin(admin.ModelAdmin):
    list_display = (
        'dni',
        'nombres',
        'apellidos',
        'correo',
        'cargo',
        'area',
        'rol',
        'activo',
    )

    search_fields = (
        'dni',
        'nombres',
        'apellidos',
        'correo',
    )

    list_filter = (
        'rol',
        'area',
        'activo',
    )