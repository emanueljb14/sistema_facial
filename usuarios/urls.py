from django.urls import path
from . import views

# Espacio de nombres de la aplicación
app_name = 'usuarios'

urlpatterns = [
    path('', views.lista_trabajadores, name='lista_trabajadores'),
    path('registro/', views.registro, name='registro'),  # Coincide con {% url 'usuarios:registro' %}
    path('login/', views.iniciar_sesion, name='login'),      # Coincide con {% url 'usuarios:login' %}
    path('logout/', views.cerrar_sesion, name='logout'),    # Coincide con {% url 'usuarios:logout' %}
    path('perfil/', views.perfil, name='perfil'),
]