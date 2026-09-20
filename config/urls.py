from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [

    # ========================================================
    # ADMINISTRACIÓN
    # ========================================================

    path('admin/', admin.site.urls),


    # ========================================================
    # DASHBOARD
    # ========================================================

    path('', include('dashboard.urls')),


    # ========================================================
    # USUARIOS
    # ========================================================

    path('usuarios/', include('usuarios.urls')),


    # ========================================================
    # RECONOCIMIENTO FACIAL
    # ========================================================

    path('reconocimiento/', include('reconocimiento.urls')),


    # ========================================================
    # ASISTENCIAS
    # ========================================================

    path('asistencias/', include('asistencias.urls')),
]


# ============================================================
# ARCHIVOS MULTIMEDIA
# ============================================================

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )