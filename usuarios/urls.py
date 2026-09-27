from django.urls import path

from . import views


urlpatterns = [

    path(
        '',
        views.lista_trabajadores,
        name='lista_trabajadores'
    ),

    path(
        'agregar/',
        views.registro,
        name='agregar_usuario'
    ),

    path(
        'login/',
        views.iniciar_sesion,
        name='login'
    ),

    path(
        'logout/',
        views.cerrar_sesion,
        name='logout'
    ),

    path(
        'perfil/',
        views.perfil,
        name='perfil'
    ),

]