from django.urls import path
from . import views

app_name = 'reconocimiento'

urlpatterns = [
    # Ruta principal del módulo
    path('', views.index, name='index'),
    
    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Endpoint para registrar rostros
    path('register/', views.register_face, name='register_face'),
    
    # Endpoint para validar/autenticar login facial
    path('login_face/', views.login_face, name='login_face'),
    
    # Vista pública del login facial
    path('login-facial/', views.login_facial, name='login_facial'),
]