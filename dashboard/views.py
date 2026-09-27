from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def dashboard_index(request):
    return render(request, 'dashboard/index.html')


def usuarios_index(request):
    return render(request, 'usuarios/index.html')


def reconocimiento_index(request):
    return render(request, 'reconocimiento/index.html')


def asistencias_index(request):
    return render(request, 'asistencias/index.html')


def reportes_index(request):
    return render(request, 'reportes/index.html')