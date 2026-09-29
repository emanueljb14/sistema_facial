from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # Redirige siempre al login público
    path('', lambda request: redirect('usuarios:login'), name='root'),

    # Rutas de las aplicaciones con sus respectivos namespaces
    path('dashboard/', include(('dashboard.urls', 'dashboard'), namespace='dashboard')),
    path('usuarios/', include(('usuarios.urls', 'usuarios'), namespace='usuarios')),
    path('reconocimiento/', include(('reconocimiento.urls', 'reconocimiento'), namespace='reconocimiento')),
    path('asistencias/', include(('asistencias.urls', 'asistencias'), namespace='asistencias')),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )