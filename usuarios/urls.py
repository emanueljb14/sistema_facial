
from django.urls import path

from . import views


urlpatterns = [

    # Lista de trabajadores
    path(
        '',
        views.lista_trabajadores,
        name='lista_trabajadores'
    ),

    # Registro
    path(
        'registro/',
        views.registro,
        name='registro'
    ),

    # Login
    path(
        'login/',
        views.iniciar_sesion,
        name='login'
    ),

    # Logout
    path(
        'logout/',
        views.cerrar_sesion,
        name='logout'
    ),

    # Perfil
    path(
        'perfil/',
        views.perfil,
        name='perfil'
    ),
]

