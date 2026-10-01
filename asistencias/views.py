from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    """Renderiza la pantalla principal de seguimiento de asistencias"""
    return render(request, 'asistencias/index.html')