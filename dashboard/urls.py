from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard_index, name='dashboard'),
    path('usuarios/', views.usuarios_index, name='usuarios'),
    path('reconocimiento/', views.reconocimiento_index, name='reconocimiento'),
    path('asistencias/', views.asistencias_index, name='asistencias'),
    path('reportes/', views.reportes_index, name='reportes'),
]